from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    all_time_score = models.IntegerField(default=0, verbose_name='количество очков за все время')
    all_time_high_score = models.IntegerField(default=0, verbose_name='максимальный результат за все время')
    coins = models.IntegerField(default=0, verbose_name='количество монет у пользователя')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"


class Season(models.Model):
    name = models.CharField(max_length=50, verbose_name='название сезона', blank=True)
    number = models.IntegerField(verbose_name='номер сезона')
    start_date = models.DateTimeField(verbose_name='время начала сезона')
    finish_date = models.DateTimeField(verbose_name='время окончания сезона')
    prize = models.CharField(max_length=250, blank=True, verbose_name='приз сезона')

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'

    def __str__(self):
        return f"{self.number} сезон"


class UserSeasonScore(models.Model):
    # related_name позволяет назначать имя атрибуту, который используется для связи от ассоциированного объекта назад к нему.
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_score')
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE, related_name='season_score')
    season_high_score = models.IntegerField(default=0, verbose_name='максимальный результат пользователя в сезоне')

    class Meta:
        verbose_name = 'Результат за сезон'
        verbose_name_plural = 'Результаты за сезоны'

    def __str__(self):
        return f"Результаты за сезон № {self.season.number} игрока {self.user.username}"

