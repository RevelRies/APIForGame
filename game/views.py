from .models import User, Season, UserSeasonScore
from accounts.permissions import IsOwner
from .serializers import (UserDataSerializer,
                          UserSaveCoinsSerializer,
                          UserSaveScoreSerializer,
                          SeasonLeaderboardSerializer,
                          SeasonListSerializer)

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse

from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response


def get_instance(request, search_field):
    # пробуем получить search_field из тела запроса
    try:
        request.data[search_field]
    except:
        return Response({search_field: ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    # пробуем найти пользователя с таким search_field
    try:
        if search_field == 'email':
            return User.objects.get(email=request.data[search_field])
        elif search_field == 'season_number':
            return Season.objects.get(number=request.data[search_field])
    except:
        return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)


class UserDataView(APIView):
    '''
    Получение данных пользователя. Тело запроса:\n
    {\n
    "email": "youremail@mail.ru"\n
    }\n
    '''

    # указывает что ответ могут получить только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter('Request body',
                             OpenApiTypes.OBJECT,
                             OpenApiParameter.QUERY,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value={
                                         "email": "youremail@mail.ru",
                                     }
                                 )
                             ]
                             ),
        ],
        summary='Данные пользователя',
        description='Возвращает все данные пользователя',
        responses={
            200: OpenApiResponse(
                'Информация об объекте',
                examples=[
                    OpenApiExample(
                        'Успешно',
                        value={
                            "email": "ayzikov1@gmail.com",
                            "username": "ayzo3",
                            "all_time_score": 0,
                            "all_time_high_score": 0,
                            "coins": 0
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request: Request):
        user = get_instance(request, 'email')
        serializer = UserDataSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SaveScoreView(APIView):
    '''
    Изменение all_time_score, all_time_high_score и season_high_score для пользователя. Тело запроса:\n
    {\n
    "email": "youremail@mail.ru",\n
    "score": "250"\n
    }\n
    '''
    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter('Request body',
                             OpenApiTypes.OBJECT,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value={
                                         "email": "youremail@mail.ru",
                                         "score": 250
                                     }
                                 )
                             ]
                             ),
        ],
        summary='Изменение score',
        description='Изменение all_time_score, all_time_high_score и season_high_score для пользователя',
        responses={
            200: OpenApiResponse(
                'Информация об объекте',
                examples=[
                    OpenApiExample(
                        'Score изменен',
                        value={
                            "email": "ayzikov1@mail.ru",
                            "score": "добавленные очки"
                        }
                    )
                ]
            ),
        },
    )
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
    Изменение coins пользователя. Тело запроса:\n
    {\n
    "email": "youremail@mail.ru",\n
    "coins": 15\n
    }\n
    '''

    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter('Request body',
                             OpenApiTypes.OBJECT,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value={
                                         "email": "youremail@mail.ru",
                                         "coins": 250
                                     }
                                 )
                             ]
                             ),
        ],
        summary='Изменение coins',
        description='Изменение coins для пользователя',
        responses={
            200: OpenApiResponse(
                'Информация об объекте',
                examples=[
                    OpenApiExample(
                        'Coins изменены',
                        value={
                            "email": "ayzikov1@mail.ru",
                            "coins": "Количество coins пользователя после изменения"
                        }
                    )
                ]
            ),
        },
    )
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
    Положение пользователя в лидербордах всех сезонов. Тело запроса:\n
    {\n
    "email": "youremail@mail.ru",\n
    }\n
    '''

    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

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

    @extend_schema(
        parameters=[
            OpenApiParameter('Request body',
                             OpenApiTypes.OBJECT,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value={
                                         "email": "youremail@mail.ru",
                                     }
                                 )
                             ]
                             ),
        ],
        summary='Лидерборд пользователя',
        description='Положение пользователя в лидербордах всех сезонов',
        responses={
            200: OpenApiResponse(
                'Информация об объекте',
                examples=[
                    OpenApiExample(
                        'Успешный успех',
                        value={
                            "season_1": {
                                "season_name": "название сезона",
                                "season_number": "номер сезона",
                                "user_position": "место пользователя в этом сезоне"
                            },
                            "season_2": {
                                "season_name": "testseason2",
                                "season_number": 2,
                                "user_position": 4
                            },
                            "season_3": {
                                "season_name": "testseason3",
                                "season_number": 3,
                                "user_position": 5
                            }
                        }
                    )
                ]
            ),
        },
    )
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


class SeasonLeaderboard(generics.ListAPIView):
    '''
    Получаем лидерборд сезона. Тело запроса:\n
    {\n
    "season_number": 3,\n
    }\n
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = SeasonLeaderboardSerializer

    def get_queryset(self):
        '''
        Переопределяю метод для проверки тела запроса и вывода UserSeasonScore для данного сезона
        '''
        try:
            season_number = self.request.data['season_number']
        except:
            return Response({"season_number": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            season = Season.objects.get(number=season_number)
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        return UserSeasonScore.objects.filter(season=season.id).order_by('-season_high_score', 'user__username')


class SeasonList(generics.ListAPIView):
    '''
    Получаем список сезонов. Тело запроса:\n
    В тело запроса передавать ничего не требуется
    '''

    queryset = Season.objects.all().order_by('number')
    serializer_class = SeasonListSerializer
    permission_classes = (IsAuthenticated,)