from django.utils import timezone

from .models import User, Season, UserSeasonScore
from .serializers import (UserDataSerializer,
                          SaveUserDataSerializer,
                          SeasonTopLeaderboardSerializer,
                          SeasonCurrentLeaderboardSerializer,
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
                            order_by("-season_high_score"))

    return list(user_season_score_qs.values_list('id', flat=True)).index(current_user_season_score.id) + 1

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
            OpenApiParameter(
                name="email",
                description=("Email пользователя"),
                default="admin@admin.ru",
                type=str,
            ),
        ],
        summary='Данные пользователя',
        description='Возвращает все данные пользователя'
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
                "unlocked_characters": serializers.JSONField(default=dict())
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


class UserLeaderboardAllSeasonPosition(APIView):
    '''
    Положение пользователя в лидербордах всех сезонов.
    '''

    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                description=("Email пользователя"),
                default="admin@admin.ru",
                type=str,
            ),
        ],
        summary='Лидерборд пользователя ВСЕ СЕЗОНЫ',
        description='Положение пользователя в лидербордах всех сезонов',
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


class UserLeaderboardCurrentSeasonPosition(generics.ListAPIView):
    '''
        Положение пользователя в текущем сезоне.
    '''

    # указывает что запрос могут сделать только авторизованные пользователи
    permission_classes = (IsAuthenticated,)
    serializer_class = SeasonCurrentLeaderboardSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                description=("Email пользователя"),
                default="admin@admin.ru",
                type=str,
            ),
            OpenApiParameter(
                name="count_around",
                description=("Количество пользователей до и после указанного пользователя"),
                default=3,
                type=int,
            ),
        ],
        summary='Лидерборд пользователя ТЕКУЩИЙ СЕЗОНЫ',
        description='Положение пользователя в лидерборде текущего сезонона. Если count_around не передан по дефолту он равен 3',
    )

    def get_queryset(self):
        email = self.request.GET.get('email', None)
        count_around = int(self.request.GET.get('count_around', 3))
        season = Season.objects.filter(
            start_date__lte=timezone.now(),
            finish_date__gte=timezone.now()
        ).first()

        # пробуем получить email из заголовков запроса
        if not email:
            return Response({"email": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # пробуем найти пользователя с таким email
        try:
            user = User.objects.get(email=email)
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем индекс пользователя в списке QS
        user_season_position_in_qs = get_user_position(season=season, user=user) - 1

        # число пользователей в сезоне
        count_users_season = UserSeasonScore.objects.filter(season=season.id).order_by('-season_high_score').count()

        # Вычисляем срез пользователей которых нужно показывать
        if user_season_position_in_qs - count_around < 0:
            start = 0
        else:
            start = user_season_position_in_qs - count_around

        if user_season_position_in_qs + count_around + 1 > count_users_season:
            finish = count_users_season
        else:
            finish = user_season_position_in_qs + count_around + 1

        # QS всех пользователей в лидерборде
        return UserSeasonScore.objects.filter(season=season.id).order_by('-season_high_score')[start:finish]





@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="season_number",
                description=("Номер сезона"),
                default=3,
                type=int,
            ),
            OpenApiParameter(
                name="top_size",
                description=("Количество топ игроков"),
                default=5,
                type=int,
            )
        ],
        summary='Топ игроков сезона',
        description='Если не передавать параметры, то по умолчанию выбирается текущий сезон и топ 5 игроков',
    )
)
class SeasonTopLeaderboard(generics.ListAPIView):
    '''
    Получаем лидерборд сезона. Тело запроса:\n
    {\n
    "season_number": 3,\n
    }\n
    '''

    permission_classes = (IsAuthenticated,)
    serializer_class = SeasonTopLeaderboardSerializer

    def get_queryset(self):
        '''
        Переопределяю метод для проверки тела запроса и вывода топа игроков для текущего сезона
        '''

        # получаем номер сезона из параметров запроса
        season_number = self.request.GET.get('season_number', None)
        if not season_number:
            season_number = Season.objects.filter(
                start_date__lte=timezone.now(),
                finish_date__gte=timezone.now()
            ).first().number

        # получаем количество топа игроков которых нужно вывести
        top_size = int(self.request.GET.get('top_size', 5))

        # пробуем найти сезон с таким номером
        try:
            season = Season.objects.get(number=season_number)
        except:
            return Response({"error": "Object does not exists"}, status=status.HTTP_400_BAD_REQUEST)

        return UserSeasonScore.objects.filter(season=season.id).order_by('-season_high_score')[:top_size]


@extend_schema_view(
    get=extend_schema(
        summary='Список всех сезонов',
        description='Возвращает список всех сезонов. Для запроса ничего передавать не надо',
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