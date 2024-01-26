from django.contrib import admin

from .models import UserSeasonScore, UserProfile, Season

admin.site.register(UserProfile)
admin.site.register(UserSeasonScore)
admin.site.register(Season)
