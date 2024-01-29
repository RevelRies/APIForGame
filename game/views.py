from .models import User
from .serializers import UserDataSerializer, UserSaveCoinsSerializer

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
    pass


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


