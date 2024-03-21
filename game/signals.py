import os
from datetime import timedelta

from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save

from .models import User, Season, UserSeasonScore, Booster, Prize, Rank
from .additional_functions import calculate_image_hash


@receiver(pre_save, sender=Season)
def checking_existing_season_data(sender, instance, **kwargs):
    '''
    Функция перед сохранением сезона проверяет не пересекается ли сезон по времени с другими сезонами
    + проверяет чтобы у каждого сезона при сохранении был создан приз для каждого ранга
    '''

    # если это новый сезон
    if not Season.objects.filter(number=instance.number).exists():
        # создание самого первого сезона
        if not Season.objects.all().exists():
            instance.number = 1
            instance.is_active = True
            # проверяем чтобы дата начала была не позже сегодня
            if instance.start_date > (timezone.localtime(timezone.now())).date():
                instance.start_date = (timezone.localtime(timezone.now())).date()
        # создание не первого сезона
        else:
            prev_season = Season.objects.all().last()
            instance.number = prev_season.number + 1
            # проверка чтобы дата начала у нового сезона была после даты конца пред сезона
            if instance.start_date != prev_season.finish_date + timedelta(days=1):
                instance.start_date = prev_season.finish_date + timedelta(days=1)
        # проверка чтобы дата конца сезона была после даты его начала
        if instance.finish_date <= instance.start_date:
            instance.finish_date = instance.start_date + timedelta(days=60)

    # если это редактирование существующего сезона
    else:
        last_season_number = Season.objects.all().last().number

        # проверка чтобы дата конца сезона была после даты его начала
        if instance.finish_date <= instance.start_date:
            instance.finish_date = instance.start_date + timedelta(days=60)

        # если это первый сезон - проверяем чтобы дата начала была не позже сегодня
        if instance.number == 1:
            if instance.start_date > (timezone.localtime(timezone.now())).date():
                instance.start_date = (timezone.localtime(timezone.now())).date()

        # если это первый и не последний сезон - проверяем чтобы дата конца была до начала 2 сезона
        if instance.number == 1 and last_season_number != 1:
            instance.finish_date = Season.objects.get(number=2).start_date - timedelta(days=1)

        # если это сезон, который находится между двумя - проверяем чтобы дата начала не совпадала с датой конца
        # предыдущего сезона и дата конца не совпадала с датой начала следующего сезона
        elif last_season_number != instance.number:
            instance.start_date = Season.objects.get(number=instance.number - 1).finish_date + timedelta(days=1)
            instance.finish_date = Season.objects.get(number=instance.number + 1).start_date - timedelta(days=1)

        # если это последний сезон и он не первый - проверяем чтобы дата начала не совпадала с датой конца предыдущего сезона
        elif last_season_number == instance.number and last_season_number != 1:
            instance.start_date = Season.objects.get(number=instance.number - 1).finish_date + timedelta(days=1)

    # # проверка создания всех призов для каждого ранга в сезоне
    # for rank in Rank.objects.all():
    #     if not Prize.objects.get(rank=rank, season=instance).exists():
    #         raise



@receiver(post_save, sender=Season)
def create_user_season_score(sender, instance, created, **kwargs):
    '''
    Функция создает UserSeasonScore для каждого пользователя при создании нового сезона
    '''
    if created:
        # создание UserSeasonScore
        for user in User.objects.all():
            UserSeasonScore.objects.create(user=user,
                                           season=instance)


@receiver(post_save, sender=User)
def create_new_user_season_score(sender, instance, created, **kwargs):
    '''
    Функция создает UserSeasonScore для текущего сезона только что зарегистрировавшегося пользователя
    + добавляет в поле booster json с существующими бустерами
    '''

    # Выбирает текущий сезон
    # Обернуто для миграций
    # После добавленеия поля is_active в Season модель почему-то из-за этих строк не выполняются миграции
    try:
        current_season = Season.objects.get(is_active=True)
    except:
        pass

    # JSON с существующими бустерами
    boosters_dict = dict()
    for booster in Booster.objects.all():
        boosters_dict[booster.string_id] = 0

    if created:
        # создание UserSeasonScore для пользователя
        UserSeasonScore.objects.create(
            user=instance,
            season=current_season
        )

        # добавление json с бустерами в поле boosters пользователя
        instance.boosters = boosters_dict
        instance.save()


@receiver(post_save, sender=Booster)
def create_new_user_season_score(sender, instance, created, **kwargs):
    '''
    При создании нового бустера он добавляется в поле boosters всех пользователей и призов
    '''

    if created:
        for user in User.objects.all():
            user.boosters[instance.string_id] = 0
            user.save()

        for prize in Prize.objects.all():
            prize.boosters[instance.string_id] = 0
            prize.save()

@receiver(post_delete, sender=Booster)
def delete_booster_from_user(sender, instance, **kwargs):
    '''
    При удалении бустера у всех пользователей и призов этот бустер удаляется из модели
    '''

    for user in User.objects.all():
        del user.boosters[instance.string_id]
        user.save()

    for prize in Prize.objects.all():
        del prize.boosters[instance.string_id]
        prize.save()


@receiver(post_save, sender=Rank)
def check_hash(sender, instance, created, **kwargs):
    '''
    Записывает хэш сохраненного изображения
    '''

    # вычисляем хэш загруженной картинки с сравниваем с хэшом в БД
    image_hash_current = calculate_image_hash(instance)
    image_hash_db = instance.image_hash

    # если хэши отличаются - значит загружена новая картинка и мы записываем новый хэш и дату загрузки
    if image_hash_current != image_hash_db:

        Rank.objects.filter(id=instance.id).update(image_hash=image_hash_current,
                                                   image_datetime=timezone.localtime(timezone.now()))


