import uuid
import os
from dotenv import load_dotenv
load_dotenv()

from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser, UserManager



class CustomUserManager(UserManager):
    '''
    Переопределяем стандартный UserManager для того чтобы, сделать поле username не обязательным для ввода
    Поле username будет генерироваться автоматически
    '''

    def _get_email(self, email: str):
        ''' Функция проверяет email на правильность'''
        validate_email(email)
        return email

    def _generate_username(self):
        ''' Функция рандомно генерирует username для каждого нового пользователя '''
        return uuid.uuid4()

    def _create_user(self, email, password, username, commit, is_staff=False, is_superuser=False):
        ''' Переопределение функции чтобы, убрать обязательный ввод username '''
        email = self._get_email(email)

        # # если пользователь входил через сторонние сервисы (Google или Apple), то ему устанавливается username указанный в его профиле сервиса
        if not username:
            username = self._generate_username()

        user = User(email=email, username=username, is_staff=is_staff, is_superuser=is_superuser)

        # если пользователь входил через сторонние сервисы (Google или Apple), то ему устанавливается стандартный пароль
        if not password:
            password = os.getenv('DEFAULT_PASSWORD')

        user.set_password(password)

        if commit:
            user.save()

        return user

    def create_user(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("commit", True)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("commit", True)

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='логин пользователя')
    all_time_score = models.IntegerField(default=0, verbose_name='количество очков за все время')
    all_time_high_score = models.IntegerField(default=0, verbose_name='максимальный результат за все время')
    coins = models.IntegerField(default=0, verbose_name='количество монет у пользователя')

    # строка необходима для использования CustomUserManager в запросах
    objects = CustomUserManager()

# обозначаем что в поле username теперь должен быть email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f"Профиль пользователя {self.username}"


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

