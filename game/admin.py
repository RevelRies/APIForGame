from django.contrib import admin

from .models import UserSeasonScore, User, Season, Character, Booster, Rank, Prize
from .validator_forms import SeasonValidationForm

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


class PrizesInline(admin.StackedInline):
    '''
    Класс для создания призов внутри модели сезона
    '''

    model = Prize
    max_num = 3
    can_delete = False


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    # функции добавлены для изменения отображения времени в админке
    def start_time_seconds(self, obj):
        return obj.start_time.strftime("%H:%M")
    start_time_seconds.admin_order_field = 'timefield'
    start_time_seconds.short_description = 'время начала сезона'

    def finish_time_seconds(self, obj):
        return obj.finish_time.strftime("%H:%M")
    finish_time_seconds.admin_order_field = 'timefield'
    finish_time_seconds.short_description = 'время окончания сезона'

    def season_name(self, obj):
        return f"{obj.number} Сезон"
    season_name.admin_order_field = 'string'
    season_name.short_description = 'Сезон'

    form = SeasonValidationForm
    # определяет какие поля отображать в главном меню сезонов
    list_display = ['season_name', 'is_active', 'start_date', 'finish_date']
    # определяет поля которые не нужно отображать
    exclude = ['start_time', 'finish_time']
    # сезоны будут автоматически сортироваться по number
    ordering = ['-number']
    # поля только для чтения
    readonly_fields = ['number', 'start_time_seconds', 'finish_time_seconds', 'is_active']
    #
    inlines = [PrizesInline]


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    # сезоны будут автоматически сортироваться по number
    ordering = ['-name']


@admin.register(Booster)
class BoosterAdmin(admin.ModelAdmin):
    # сезоны будут автоматически сортироваться по number
    ordering = ['-name']


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    ordering = ['number']


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    ordering = ['-season__number', 'rank__number']
