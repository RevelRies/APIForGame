from game.models import User

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer, UserDataSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class SingUpView(APIView):
    '''
    Для регистрации пользователя в теле запроса нужно передать:\n
    {"email": "youremail@google.com"}\n
    {"password": "yourpassword"}\n
    При успешной регистрации вернется {"result": "Пользователь зарегистрирован"}
    '''
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'Пользователь зарегистрирован'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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






