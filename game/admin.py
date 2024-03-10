from django.contrib import admin

from .models import UserSeasonScore, User, Season, Character, Booster

import json
import logging

from django.db.models import JSONField
from django.forms import widgets

logger = logging.getLogger(__name__)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # пользователи будут автоматически сортироваться по username
    ordering = ['username']
    # определяет боковую панель с полями по которым можно включить фильтрацию
    list_filter = ['username', 'date_joined']
    # определяет поля которые не нужно отображать
    exclude = ['refresh_token', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'password',
               'last_login', 'user_permissions', 'groups', 'is_superuser', 'score']


@admin.register(UserSeasonScore)
class UserSeasonScoreAdmin(admin.ModelAdmin):
    # результаты будут сортироваться по номеру сезона и username
    ordering = ['-season__number', 'user__username']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    # сезоны будут автоматически сортироваться по number
    ordering = ['-number']


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    # сезоны будут автоматически сортироваться по number
    ordering = ['-name']


@admin.register(Booster)
class BoosterAdmin(admin.ModelAdmin):
    # сезоны будут автоматически сортироваться по number
    ordering = ['-name']
