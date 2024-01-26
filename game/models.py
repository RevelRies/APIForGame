from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    all_time_score = models.IntegerField(default=0, verbose_name='количество очков за все время')
    all_time_high_score = models.IntegerField(default=0, verbose_name='максимальный результат за все время')
    coins = models.IntegerField(default=0, verbose_name='количество монет у пользователя')


class Season(models.Model):
    name = models.CharField(max_length=50, verbose_name='название сезона')
    number = models.IntegerField(verbose_name='номер сезона')
    start_date = models.DateTimeField(verbose_name='время начала сезона')
    finish_date = models.DateTimeField(verbose_name='время окончания сезона')
    prize = models.CharField(max_length=250, blank=True, verbose_name='приз сезона')


class UserSeasonScore(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE)
    season_high_score = models.IntegerField(default=0, verbose_name='максимальный результат пользователя в сезоне')

