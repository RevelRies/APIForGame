from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Season, UserSeasonScore

@receiver(post_save, sender=Season)
def create_user_season_score(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            UserSeasonScore.objects.create(user=user,
                                           season=instance)