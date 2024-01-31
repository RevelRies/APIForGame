from .models import User, Season, UserSeasonScore

from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'all_time_score', 'all_time_high_score', 'coins']


class UserSaveCoinsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'coins']

    def update(self, instance, validated_data):
        # instanse - это объект User
        instance.coins += validated_data['coins']
        instance.save()
        return instance


class UserSaveScoreSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'score']

    def update(self, instance, validated_data):
        # score который передал фронт в запросе
        score = validated_data['score']
        instance.score = score

        all_time_high_score = instance.all_time_high_score
        now = timezone.now()
        current_season = Season.objects.get(start_date__lte=now, finish_date__gte=now)
        user_season_score = UserSeasonScore.objects.get(user=instance, season=current_season)

        # обновление общих очков пользователя за все время
        instance.all_time_score += score

        # обновление максимального результата пользователя за все время
        if all_time_high_score < score:
            instance.all_time_high_score = score

        # обновление максимального результата пользователя за текущий сезон
        if user_season_score.season_high_score < score:
            user_season_score.season_high_score = score

        # сохраняем User и UserSeasonScore после изменений
        instance.save()
        user_season_score.save()

        return instance










