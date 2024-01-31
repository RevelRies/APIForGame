from game.models import User

from social_django.models import UserSocialAuth

from .serializers import UserSerializer, ChangeUsernameSerializer
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
            return Response({'result': 'registration was successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получение данных Google профиля пользователя

        # В данной строке происходит извлечение данных из Google и регистрация пользователя в нашей БД
        user_social = UserSocialAuth.objects.get(user=request.user, provider='google-oauth2')

        data = {
            'username': request.user.username,
            'email': user_social.extra_data['email'],
            'google_id': user_social.uid,
        }
        return Response(data)


class ChangeUsernameView(APIView):
    '''
    API для изменения username пользователя
    '''

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
        serializer = ChangeUsernameSerializer(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            result_data = {"result": "the user's username has been successfully changed"}
            result_data.update(serializer.data)
            return Response(result_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)