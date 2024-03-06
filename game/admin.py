from django.contrib import admin

from .models import UserSeasonScore, User, Season, Character, Booster

import json
import logging

from django.db.models import JSONField
from django.forms import widgets

logger = logging.getLogger(__name__)


class PrettyJSONWidget(widgets.Textarea):
    def format_value(self, value):
        try:
            value = json.dumps(json.loads(value), indent=2, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            row_lengths = [len(r) for r in value.split('\n')]
            self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            return value
        except Exception as e:
            logger.warning("Error while formatting JSON: {}".format(e))
            return super(PrettyJSONWidget, self).format_value(value)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # пользователи будут автоматически сортироваться по username
    ordering = ['username']
    # определяет боковую панель с полями по которым можно включить фильтрацию
    list_filter = ['username', 'date_joined']

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget}
    }


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
