import uuid
import os

from dotenv import load_dotenv
load_dotenv()

from datetime import timedelta

from jsonschema import validate, ValidationError as JSONSchemaValidationError

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
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
        return str(uuid.uuid4()).split('-')[0]

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

        return self._create_user(email, password, username=None, **extra_fields)


class User(AbstractUser):
    def validate_json_keys(value):
        '''
        Функция добавляет проверку для ключей поля boosters
        Ключи могут содержать только string_id существующих бустеров
        '''
        allowed_keys = list()

        for booster in Booster.objects.all():
            allowed_keys.append(booster.string_id)

        if not set(value.keys()).issubset(allowed_keys):
            raise ValidationError("В JSON могут быть только string_id существующих бустеров")

    email = models.EmailField(unique=True, verbose_name='логин')
    score = models.IntegerField(default=0, verbose_name='текущие очки для сериализатора')
    all_time_score = models.IntegerField(default=0, verbose_name='количество очков за все время')
    all_time_high_score = models.IntegerField(default=0, verbose_name='максимальный результат за все время')
    coins = models.IntegerField(default=0, verbose_name='количество монет')
    deaths = models.IntegerField(default=0, verbose_name='количества смертей')
    obstacle_collisions = models.IntegerField(default=0, verbose_name='количества столкновений')
    boosters = models.JSONField(default=dict(), verbose_name='бустеры', blank=True, validators=[validate_json_keys])
    selected_character = models.CharField(default='DefaultCharacter', max_length=250, verbose_name='выбранный персонаж')
    unlocked_characters = models.JSONField(default=['DefaultCharacter', 'Girl'], verbose_name='персонажи пользователя', blank=True)

    # поле в котором хранится действительный refresh token
    refresh_token = models.CharField(default='None', max_length=500, verbose_name='действительный refresh token')

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

    def clean(self):
        # функция переопределяется для проверки поля boosters у User
        # значение любого ключа в этом поле должно быть int
        super().clean()
        schema = {
            "type": "object",
            "additionalProperties": {"type": "integer"}
        }
        try:
            validate(instance=self.boosters, schema=schema)
        except JSONSchemaValidationError as e:
            raise ValidationError(f"Неверный формат JSON: {e.message}")


class Season(models.Model):
    name = models.CharField(max_length=50, verbose_name='название сезона', blank=True)
    number = models.IntegerField(verbose_name='номер сезона')
    start_date = models.DateTimeField(default=timezone.now(), verbose_name='время начала сезона')
    finish_date = models.DateTimeField(default=timezone.now() + timedelta(days=60), verbose_name='время окончания сезона')
    prize = models.CharField(max_length=250, blank=True, verbose_name='приз сезона')
    is_active = models.BooleanField(default=False, verbose_name='текущий сезон')

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'

    def __str__(self):
        return f"{self.number} сезон"


class UserSeasonScore(models.Model):
    # related_name позволяет назначать имя атрибуту, который используется для связи от ассоциированного объекта назад к нему.
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user_score')
    season = models.ForeignKey(to=Season, on_delete=models.CASCADE, related_name='season_score')
    season_high_score = models.IntegerField(default=0, verbose_name='сумма очков пользователя в сезоне')

    class Meta:
        verbose_name = 'Результат за сезон'
        verbose_name_plural = 'Результаты за сезоны'

    def __str__(self):
        return f"Результаты за сезон № {self.season.number} игрока {self.user.username}"


class Character(models.Model):
    string_id = models.CharField(max_length=250, verbose_name='frontend id')
    name = models.CharField(max_length=250, verbose_name='имя')
    description = models.CharField(max_length=500, verbose_name='описание')
    price = models.IntegerField(verbose_name='цена')
    game_over_messages = models.JSONField(default=['message_1', 'message_2'], verbose_name='game_over_messages', blank=True)

    class Meta:
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'

    def __str__(self):
        return f"{self.name}"


class Booster(models.Model):
    string_id = models.CharField(max_length=250, verbose_name='frontend type')
    name = models.CharField(max_length=250, verbose_name='название')
    description = models.CharField(max_length=500, verbose_name='описание')
    price = models.IntegerField(verbose_name='цена')

    # default = {Invincibility  Speed  Magnet}
    class Meta:
        verbose_name = 'Бустер'
        verbose_name_plural = 'Бустеры'

    def __str__(self):
        return f"{self.string_id}"