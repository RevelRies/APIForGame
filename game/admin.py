from django.contrib import admin

from .models import UserSeasonScore, User, Season

@admin.register(User)
class UserPost(admin.ModelAdmin):
    # пользователи будут автоматически сортироваться по username
    ordering = ['username']
    # определяет боковую панель с полями по которым можно включить фильтрацию
    list_filter = ['username', 'date_joined']


@admin.register(UserSeasonScore)
class UserSeasonScorePost(admin.ModelAdmin):
    # пользователи будут автоматически сортироваться по username
    ordering = ['-season__number', 'user__username']

@admin.register(Season)
class SeasonPost(admin.ModelAdmin):
    # пользователи будут автоматически сортироваться по username
    ordering = ['-number']
