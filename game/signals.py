
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import User, Season, UserSeasonScore, Booster

@receiver(post_save, sender=Season)
def create_user_season_score(sender, instance, created, **kwargs):
    '''
    Функция создает UserSeasonScore для каждого пользователя при создании нового сезона
    '''
    if created:
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
        current_season = Season.objects.filter(
            start_date__lte=timezone.now(),
            finish_date__gte=timezone.now()
        ).first()
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
    При создании нового бустера он добавляется в поле boosters всех пользователей
    '''

    if created:
        for user in User.objects.all():
            user.boosters[instance.string_id] = 0
            user.save()


@receiver(post_delete, sender=Booster)
def delete_booster_from_user(sender, instance, **kwargs):
    '''
    При удалении бустера у всех пользователей этот бустер удаляется из модели
    '''

    for user in User.objects.all():
        del user.boosters[instance.string_id]
        user.save()