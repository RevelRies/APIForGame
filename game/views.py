from .models import User, Season, UserSeasonScore
from .serializers import (UserDataSerializer,
                          SaveUserDataSerializer,
                          SeasonLeaderboardSerializer,
                          SeasonListSerializer)

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (extend_schema,
                                   extend_schema_view,
                                   OpenApiParameter,
                                   OpenApiExample,
                                   OpenApiResponse,
                                   inline_serializer)

from rest_framework import status, generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response


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
                            order_by("season_high_score").
                            filter(season_high_score__gte=current_user_season_score.season_high_score).
                            order_by("user__username").
                            values())

    # если у нас оказалось несколько пользователей с одинаковыми season_high_score
    # тогда их позиция в лидерборде определяется в алфавитном порядке их username
    for user_position, user_season_score in enumerate(user_season_score_qs, start=1):
        if user_season_score['user_id'] == user.id:
            return user_position

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
            OpenApiParameter('Headers values',
                             OpenApiTypes.OBJECT,
                             OpenApiParameter.QUERY,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value='email=admin@admin.ru'
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
        email = request.GET.get('email', None)

        # пробуем получить email из заголовков запроса
        if not email:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            instance = User.objects.get(email=email)
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserDataSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaveUserDataView(APIView):
    '''
    Изменение всех игровых полей пользователя. Тело запроса:\n
    {\n
    "email": "youremail@mail.ru",\n
    "score": 250,\n
    "coins": 10,\n
    "deaths": 2,\n
    "obstacle_collisions": 6,\n
    "boosters": {}\n
    }\n
    '''

    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=inline_serializer(
            name="SaveUserDataDocSerializer",
            fields={
                "email": serializers.CharField(default='testemail_01@mail.ru'),
                "score": serializers.IntegerField(default=100),
                "coins": serializers.IntegerField(default=20),
                "deaths": serializers.IntegerField(default=1),
                "obstacle_collisions": serializers.IntegerField(default=5),
                "boosters": serializers.JSONField(default=dict()),
            },
        ),
        summary='Изменение игровых данных пользователя',
        description='Изменение all_time_score, all_time_high_score и season_high_score, coins, deaths, obstacle_collisions и boosters пользователя',
        responses={
            200: OpenApiResponse(
                'Информация об объекте',
                examples=[
                    OpenApiExample(
                        'Score изменен',
                        value={
                            "email": "ayzikov1@mail.ru",
                            "result": "successfully"
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

        serializer = SaveUserDataSerializer(data=request.data, instance=instance)
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
        email = self.request.GET.get('email', None)

        # пробуем получить email из заголовков запроса
        if not email:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            instance = User.objects.get(email=email)
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)


        # создаем dict в которм ключи будут "season_(номер сезона), а значения dict с данными пользователя в этом сезоне"
        result_data = dict()
        for season in Season.objects.order_by("number"):
            try:
                result_data.update(
                    {f"season_{season.number}": {
                        "season_name": season.name,
                        "season_number": season.number,
                        "user_position": get_user_position(user=instance, season=season)
                    }}
                )
            except:
                continue
        return Response(result_data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter('Headers params',
                             OpenApiTypes.OBJECT,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value='email=admin@admin.ru'
                                 )
                             ]
                             ),
        ],
        summary='Лидерборд сезона',
        description='Лидерборд сезона',
    )
)
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

        season_number = self.request.GET.get('season_number', None)
        if not season_number:
            return Response({"season_number": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            season = Season.objects.get(number=season_number)
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        return UserSeasonScore.objects.filter(season=season.id).order_by('-season_high_score', 'user__username')


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter('Request body',
                             OpenApiTypes.OBJECT,
                             examples=[
                                 OpenApiExample(
                                     'Пример запроса',
                                     value={}
                                 )
                             ]
                             ),
        ],
        summary='Список всех сезонов',
        description='Список сезонов',
    )
)
class SeasonList(generics.ListAPIView):
    '''
    Получаем список сезонов. Тело запроса:\n
    В тело запроса передавать ничего не требуется
    '''

    queryset = Season.objects.all().order_by('number')
    serializer_class = SeasonListSerializer
    permission_classes = (IsAuthenticated,)