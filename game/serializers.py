from .models import User, Season, UserSeasonScore, Booster, Character, Rank, Prize, PrizeTop3, SuperPrize

from django.utils import timezone

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

def get_user_position(user: User, season: Season):
    '''
    Получаем позицию пользователя в сезоне в соответствии с его season_high_score
    '''
    current_user_season_score = UserSeasonScore.objects.get(season=season, user=user)

    # получаем словарь из объектов QuerySet
    # фильтрация происходит в таком порядке
    # 1 - QS текущего сезона
    # 2 - фильтруем по убыванию season_high_score
    # 3 - QS у которых season_high_score больше либо равен season_high_score данного пользователя
    # 4 - фильтруем по username пользователей
    user_season_score_qs = (UserSeasonScore.objects.
                            filter(season=season).
                            order_by("-season_high_score"))

    return list(user_season_score_qs.values_list('id', flat=True)).index(current_user_season_score.id) + 1

class UserDataSerializer(ModelSerializer):
    season_high_score = serializers.SerializerMethodField()
    rank_number = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'username', 'all_time_score', 'all_time_high_score', 'season_high_score', 'coins', 'deaths',
                  'obstacle_collisions', 'boosters', 'selected_character', 'unlocked_characters', 'rank_number']
        extra_kwargs = {'email': {'required': False},
                        'username': {'required': False}}

    def get_season_high_score(self, user):
        current_season = Season.objects.get(is_active=True)
        user_season_score = UserSeasonScore.objects.get(user=user, season=current_season)
        return user_season_score.season_high_score

    def get_rank_number(self, user):
        try:
            return user.rank.number
        except:
            return user.rank


class SaveUserDataSerializer(ModelSerializer):
    season_high_score = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['email', 'username', 'score', 'all_time_score', 'all_time_high_score', 'season_high_score', 'coins',
                  'deaths', 'obstacle_collisions']
        extra_kwargs = {'username': {'required': False}}

    def get_season_high_score(self, user):
        current_season = Season.objects.get(is_active=True)
        user_season_score = UserSeasonScore.objects.get(user=user, season=current_season)
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

        # изменяем score
        score = validated_data['score']
        instance.score = score

        # поиск в БД текущего сезона
        all_time_high_score = instance.all_time_high_score
        current_season = Season.objects.get(is_active=True)
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


class SeasonTopLeaderboardSerializer(ModelSerializer):
    user = UserDataSerializer()

    # Обернуто для миграций
    # После добавленеия поля is_active в Season модель почему-то из-за этих строк не выполняются миграции
    try:
        season = Season.objects.get(is_active=True)
    except:
        pass

    season_position = serializers.SerializerMethodField()

    class Meta:
        model = UserSeasonScore
        fields = ['user', 'season_position']

    def get_season_position(self, user_season_score):
        return get_user_position(user=user_season_score.user, season=user_season_score.season)


class SeasonCurrentLeaderboardSerializer(ModelSerializer):
    user = UserDataSerializer()

    # Обернуто для миграций
    # После добавленеия поля is_active в Season модель почему-то из-за этих строк не выполняются миграции
    try:
        season = Season.objects.get(is_active=True)
    except:
        pass

    season_position = serializers.SerializerMethodField()
    class Meta:
        model = UserSeasonScore
        fields = ['user', 'season_position']

    def get_season_position(self, user_season_score):
        return get_user_position(user=user_season_score.user, season=user_season_score.season)


class SeasonListSerializer(ModelSerializer):
    class Meta:
        model = Season
        exclude = ['id']


class BoostersListSerializer(ModelSerializer):
    class Meta:
        model = Booster
        exclude = ['id']


class CharactersListSerializer(ModelSerializer):
    class Meta:
        model = Character
        exclude = ['id']


class RanksListSerializer(ModelSerializer):
    class Meta:
        model = Rank
        exclude = ['id']


class PrizeListSerializer(ModelSerializer):
    season_number = serializers.IntegerField(read_only=True, source='season.number')
    rank_number = serializers.IntegerField(read_only=True, source='rank.number')

    class Meta:
        model = Prize
        fields = ['season_number', 'rank_number', 'coins', 'characters', 'boosters']


class PrizeTop3ListSerializer(ModelSerializer):
    season_number = serializers.IntegerField(read_only=True, source='season.number')
    class Meta:
        model = PrizeTop3
        fields = ['season_number', 'top_number', 'coins', 'characters', 'boosters']


class SuperPrizeViewSerializer(ModelSerializer):
    season_number = serializers.IntegerField(read_only=True, source='season.number')

    class Meta:
        model = SuperPrize
        fields = ['season_number', 'name', 'image_preview', 'image_gift', 'description', 'burns_down_date']