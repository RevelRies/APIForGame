from .models import User, Season, UserSeasonScore

from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer


class UserDataSerializer(ModelSerializer):
    season_high_score = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'username', 'all_time_score', 'all_time_high_score', 'season_high_score', 'coins', 'deaths', 'obstacle_collisions', 'boosters']
        extra_kwargs = {'username': {'required': False}}

    def get_season_high_score(self, user):
        user_season_score = UserSeasonScore.objects.filter(user=user).last()
        return user_season_score.season_high_score


class SaveUserDataSerializer(ModelSerializer):
    season_high_score = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'username', 'score', 'all_time_score', 'all_time_high_score', 'season_high_score', 'coins', 'deaths', 'obstacle_collisions', 'boosters']
        extra_kwargs = {'username': {'required': False}}

    def get_season_high_score(self, user):
        user_season_score = UserSeasonScore.objects.filter(user=user).last()
        return user_season_score.season_high_score

    def to_representation(self, obj):
        ''' Переопределение функции для исключения из вывода поля score '''
        ret = super().to_representation(obj)
        ret.pop('score')
        return ret

    def update(self, instance, validated_data):
        # изменяем coins
        instance.coins += validated_data['coins']
        # изменяем deaths
        instance.deaths += validated_data['deaths']
        # изменяем obstacle_collisions
        instance.obstacle_collisions += validated_data['obstacle_collisions']
        # изменяем boosters
        if validated_data['boosters'] != {}:
            instance.boosters = validated_data['boosters']

        # изменяем score
        score = validated_data['score']
        instance.score = score

        # поиск в БД текущего сезона
        all_time_high_score = instance.all_time_high_score
        now = timezone.now()
        current_season = Season.objects.get(start_date__lte=now, finish_date__gte=now)
        user_season_score = UserSeasonScore.objects.get(user=instance, season=current_season)

        # обновление общих очков пользователя за все время
        instance.all_time_score += score

        # обновление максимального результата пользователя за все время
        if all_time_high_score < score:
            instance.all_time_high_score = score

        # обновление суммарного результата пользователя за текущий сезон
        user_season_score.season_high_score += score

        # сохраняем User и UserSeasonScore после изменений
        instance.save()
        user_season_score.save()

        return instance


class SeasonLeaderboardSerializer(ModelSerializer):
    user = UserDataSerializer()
    class Meta:
        model = UserSeasonScore
        fields = ['user']


class SeasonListSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'









