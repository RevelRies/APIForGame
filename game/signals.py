
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Season, UserSeasonScore

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
    '''

    # Выбирает текущий сезон
    current_season = Season.objects.filter(
        start_date__lte=timezone.now(),
        finish_date__gte=timezone.now()
    ).first()

    if created:
        UserSeasonScore.objects.create(
            user=instance,
            season=current_season
        )