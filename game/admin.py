from django.contrib import admin

from .models import UserSeasonScore, User, Season

admin.site.register(User)
admin.site.register(UserSeasonScore)
admin.site.register(Season)
