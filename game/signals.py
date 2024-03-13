
from django.utils import timezone
from django.db.models.signals import post_save, post_delete, pre_init
from django.dispatch import receiver

from .models import User, Season, UserSeasonScore, Booster


# @receiver(pre_init, sender=Season)
# def checking_new_season_data(sender, **kwargs):
#     '''
#     Функция перед созданием нового сезона:
#     - проверяет не пересекается ли сезон по времени с другими сезонами
#     - выставлет начальное время 00:00, а конечное 23:59
#     '''
#     new_number = kwargs['number']
#     new_start_date = kwargs['kwargs']['start_date']
#     new_finish_date = kwargs['kwargs']['finish_date']
#
#     # проверка на пересечение дат с другими сезонами

#     # если это создание не первого сезона
#     if new_number == 1:
#         raise Exception
#
#     # экземпляр предыдущего сезона
#     prev_season = Season.objects.all().last()
#
#     # если начало создаваемого сезона пересекается с концом прошлого то сезон не создается
#     if new_start_date <= prev_season.finish_date:
#         raise Exception
#
#     # новому сезону ставлю номер +1 от предыдущего
#     kwargs['kwargs']['number'] = prev_season.number + 1
#
#     # изменяю время начала и конца создаваемого сезона
#     kwargs['kwargs']['start_date'] = new_start_date.replace(hour=0, minute=0, second=0)
#     kwargs['kwargs']['finish_date'] = new_finish_date.replace(hour=23, minute=59, second=40)


@receiver(post_save, sender=Season)
def checking_season_data(sender, instance, **kwargs):
    '''
    Функция перед сохранением сезона|созданием нового:
    - проверяет не пересекается ли сезон по времени с другими сезонами
    - выставлет начальное время 00:00, а конечное 23:59
    '''

    new_start_date = instance.start_date
    new_finish_date = instance.finish_date

    # проверка на пересечение дат с другими сезонами

    # если это первый сезон, присваиваем ему #1
    if not Season.objects.all().exists():
        instance.number = 1
        instance.is_active = True
    else:
        # экземпляр предыдущего сезона
        prev_season = Season.objects.all().last()

        # новому сезону ставлю номер +1 от предыдущего
        instance.number = prev_season.number + 1

        # если начало создаваемого сезона пересекается с концом прошлого то сезон не создается
        if new_start_date <= prev_season.finish_date:
            raise Exception

    # изменяю время начала и конца создаваемого сезона
    instance.start_date = new_start_date.replace(hour=0, minute=0, second=0)
    instance.new_finish_date = new_finish_date.replace(hour=23, minute=59, second=40)



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