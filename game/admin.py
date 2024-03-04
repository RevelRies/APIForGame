from django.contrib import admin

from .models import UserSeasonScore, User, Season, Character, Booster

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # пользователи будут автоматически сортироваться по username
    ordering = ['username']
    # определяет боковую панель с полями по которым можно включить фильтрацию
    list_filter = ['username', 'date_joined']


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
