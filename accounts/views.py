from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class SingUpView(APIView):
    '''
    Для регистрации пользователя в JSON нужно передать:
    "password": "yourpassword"
    "email": "youremail@google.com"
    '''
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'Пользователь зарегистрирован'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


