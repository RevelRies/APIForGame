from .models import User, Season, UserSeasonScore
from .serializers import UserDataSerializer, UserSaveCoinsSerializer, UserSaveScoreSerializer

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response


class UserDataView(APIView):
    '''
    Получение данных пользователя
    '''

    # указывает что ответ могут получить только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request):
        '''
        Пробует получить из тела GET запроса поле email и найти пользователя с таким email.\n
        Требуется передать в теле запроса:\n
        {"email": "youremail@google.com"}\n
        Для получения информации нужно передать в заголовке:\n
        Authorization: Bearer "access token"
        '''
        try:
            email = request.data['email']
            user = User.objects.get(email=email)
            serializer = UserDataSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)


class SaveScoreView(APIView):
    '''
    Изменение all_time_score, all_time_high_score и season_high_score для пользователя
    '''
    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    def put(self, request: Request):

        # пробуем получить email из тела запроса
        try:
            request.data['email']
        except:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            instance = User.objects.get(email=request.data['email'])
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSaveScoreSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveCoinsView(APIView):
    '''
    Изменение coins пользователя
    '''

    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    def put(self, request: Request):

        # пробуем получить email из тела запроса
        try:
            request.data['email']
        except:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            instance = User.objects.get(email=request.data['email'])
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        # передаем данные в сериалайзер где уже происходит изменение coins и сохранение в БД
        serializer = UserSaveCoinsSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLeaderboardPosition(APIView):
    '''
    Положение пользователя в лидерборде всех сезонов
    '''

    def get_user_position(self, user: User, season: Season):
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
                                order_by("season_high_score").
                                filter(season_high_score__gte=current_user_season_score.season_high_score).
                                order_by("user__username").
                                values())

        # если у нас оказалось несколько пользователей с одинаковыми season_high_score
        # тогда их позиция в лидерборде определяется в алфавитном порядке их username
        for user_position, user_season_score in enumerate(user_season_score_qs, start=1):
            if user_season_score['user_id'] == user.id:
                return user_position


    def get(self, request: Request):
        # пробуем получить email из тела запроса
        try:
            request.data['email']
        except:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            instance = User.objects.get(email=request.data['email'])
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            # создаем dict в которм ключи будут "season_(номер сезона), а значения dict с данными пользователя в этом сезоне"
            result_data = dict()
            for season in Season.objects.order_by("number"):
                result_data.update(
                    {f"season_{season.number}": {
                        "season_name": season.name,
                        "season_number": season.number,
                        "user_position": self.get_user_position(user=instance, season=season)
                    }}
                )
            return Response(result_data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"error": ex}, status=status.HTTP_409_CONFLICT)

