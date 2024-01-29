from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


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






