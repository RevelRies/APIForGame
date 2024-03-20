import uuid
import os

from dotenv import load_dotenv
load_dotenv()

from datetime import datetime, timedelta, time

from jsonschema import validate, ValidationError as JSONSchemaValidationError

from django_jsonform.models.fields import JSONField

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractUser, UserManager



def get_season():
    return Season

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

        # если пользователь входил через сторонние сервисы (Google или Apple), то ему устанавливается username
        # указанный в его профиле сервиса
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


class Rank(models.Model):
    name = models.CharField(max_length=50, verbose_name='название')
    number = models.IntegerField(verbose_name='ранг по счету')
    image = models.ImageField(upload_to='ranks_images', verbose_name='изображение')
    min_int_users = models.IntegerField(verbose_name='минимальное количество пользователей (целое число)')
    min_percent_users = models.IntegerField(verbose_name='минимальное количество пользователей (проценты)')

    class Meta:
        verbose_name = 'Ранг'
        verbose_name_plural = 'Ранги'

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    def validate_boosters(value):
        '''
        Функция добавляет проверку для ключей поля boosters
        Ключи могут содержать только string_id существующих бустеров
        '''
        allowed_keys = list()

        for booster in Booster.objects.all():
            allowed_keys.append(booster.string_id)

        if set(value.keys()) != set(allowed_keys):
            raise ValidationError("В JSON должны быть все string_id существующих бустеров")

    def validate_characters(value):
        '''
        Функция добавляет проверку для персонажей пользователя
        Список персонажей пользователя может содержать только созданных персонажей
        '''
        allowed_elements = list()

        for character in Character.objects.all():
            allowed_elements.append(character.string_id)

        if not set(value).issubset(allowed_elements):
            raise ValidationError("Значениями могут быть только существующие персонажи")

    email = models.EmailField(unique=True, verbose_name='логин')
    score = models.IntegerField(default=0, verbose_name='текущие очки для сериализатора')
    all_time_score = models.IntegerField(default=0, verbose_name='количество очков за все время')
    all_time_high_score = models.IntegerField(default=0, verbose_name='максимальный результат за все время')
    coins = models.IntegerField(default=0, verbose_name='количество монет')
    deaths = models.IntegerField(default=0, verbose_name='количества смертей')
    obstacle_collisions = models.IntegerField(default=0, verbose_name='количества столкновений')
    selected_character = models.CharField(default='DefaultCharacter', max_length=250, verbose_name='выбранный персонаж')
    rank = models.ForeignKey(to=Rank, on_delete=models.CASCADE, blank=True, null=True, verbose_name='ранг')

    # поле в котором хранится действительный refresh token
    refresh_token = models.CharField(default='None', max_length=500, verbose_name='действительный refresh token')

    # определение схемы для юзерфрендли отображения в админ панели бустеров
    LABELS_SCHEMA_CHARACTERS = {
        'type': 'array',
        'items': {
            'type': 'string'
        }
    }
    unlocked_characters = JSONField(default=['DefaultCharacter', 'Girl'], verbose_name='персонажи пользователя',
                                    validators=[validate_characters], blank=True, schema=LABELS_SCHEMA_CHARACTERS)

    # определение схемы для юзерфрендли отображения в админ панели бустеров
    LABELS_SCHEMA_BOOSTERS = {
        'type': 'dict',
        "keys": {},
        'addtionalProperties': True,
        'additionalProperties': {'type': 'integer'}
}
    boosters = JSONField(default=dict(), verbose_name='бустеры', validators=[validate_boosters], blank=True,
                         schema=LABELS_SCHEMA_BOOSTERS)

    # строка необходима для использования CustomUserManager в запросах
    objects = CustomUserManager()

    # обозначаем что в поле username теперь должен быть email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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
    number = models.IntegerField(default=0, verbose_name='номер сезона')
    start_date = models.DateField(default=timezone.localtime(timezone.now()),
                                  verbose_name='дата начала сезона')
    start_time = models.TimeField(default=datetime.strptime('00:00:00', '%H:%M:%S'),
                                  verbose_name='время начала сезона')
    finish_date = models.DateField(default=(timezone.localtime(timezone.now()) + timedelta(days=60)),
                                   verbose_name='дата окончания сезона')
    finish_time = models.TimeField(default=datetime.strptime('23:59:50', '%H:%M:%S'),
                                   verbose_name='время окончания сезона')
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

    # определение схемы для юзерфрендли отображения в админ панели game_over_messages
    LABELS_SCHEMA_MESSAGES = {
        'type': 'array',
        'items': {
            'type': 'string'
        }
    }
    game_over_messages = JSONField(default=['message_1', 'message_2'], verbose_name='game_over_messages',
                                          blank=True, schema=LABELS_SCHEMA_MESSAGES)

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

    class Meta:
        verbose_name = 'Бустер'
        verbose_name_plural = 'Бустеры'

    def __str__(self):
        return f"{self.string_id}"


class Prize(models.Model):
    def validate_boosters(value):
        '''
        Функция добавляет проверку для ключей поля boosters
        Ключи могут содержать только string_id существующих бустеров
        '''
        allowed_keys = list()

        for booster in Booster.objects.all():
            allowed_keys.append(booster.string_id)

        if set(value.keys()) != set(allowed_keys):
            raise ValidationError("В JSON должны быть все string_id существующих бустеров")

    def validate_characters(value):
        '''
        Функция добавляет проверку для персонажей пользователя
        Список персонажей пользователя может содержать только созданных персонажей
        '''
        allowed_elements = list()

        for character in Character.objects.all():
            allowed_elements.append(character.string_id)

        if not set(value).issubset(allowed_elements):
            raise ValidationError("Значениями могут быть только существующие персонажи")

    season = models.ForeignKey(to=Season, on_delete=models.CASCADE, verbose_name='сезон')
    rank = models.ForeignKey(to=Rank, on_delete=models.CASCADE, verbose_name='ранг')
    coins = models.IntegerField(verbose_name='монеты')

    # определение схемы для юзерфрендли отображения в админ панели бустеров
    LABELS_SCHEMA_CHARACTERS = {
        'type': 'array',
        'items': {
            'type': 'string'
        }
    }
    characters = JSONField(default=list(), verbose_name='персонажи',
                           validators=[validate_characters], blank=True, schema=LABELS_SCHEMA_CHARACTERS)

    # определение схемы для юзерфрендли отображения в админ панели бустеров
    LABELS_SCHEMA_BOOSTERS = {
        'type': 'dict',
        "keys": {},
        'addtionalProperties': True,
        'additionalProperties': {'type': 'integer'}
    }

    # JSON с существующими бустерами
    boosters_dict = dict()
    for booster in Booster.objects.all():
        boosters_dict[booster.string_id] = 0

    boosters = JSONField(default=boosters_dict, verbose_name='бустеры', validators=[validate_boosters], blank=True,
                         schema=LABELS_SCHEMA_BOOSTERS)

    class Meta:
        verbose_name = 'Приз'
        verbose_name_plural = 'Призы'

    def __str__(self):
        return f"{self.rank.name} - сезон № {self.season.number}"
