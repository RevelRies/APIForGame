import uuid

from game.models import User

from better_profanity import profanity
from rest_framework.exceptions import APIException

profanity.load_censor_words_from_file(filename='./profanity_wordlist.txt')

from rest_framework import serializers, status
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenVerifySerializer

from django.contrib.auth import password_validation



class CustomValidation(APIException):
    ''' Кастомный обработчик ошибок сериализатора '''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: detail}
        else:
            self.detail = {'detail': self.default_detail}


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'password', 'email']


    def generate_username(self):
        ''' Функция рандомно генерирует username для каждого нового пользователя '''
        return str(uuid.uuid4()).split('-')[0]

    def create(self, validated_data):
        ''' Переопределяем метод create для того чтобы пароль сохранялся не в чистом виде, а закодированный '''
        user = User(email=validated_data['email'],
                    username=self.generate_username())

        # Проверяем пароль на валидность
        try:
            password_validation.validate_password(validated_data['password'])
        except Exception as ex:
            raise CustomValidation(ex, 'password', None)

        user.set_password(validated_data['password'])
        user.save()
        return user


class ChangeUsernameSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


    def update(self, instance, validated_data):

        if profanity.contains_profanity(validated_data['username']):
            raise serializers.ValidationError({"error": "Username contains profane words."})

        instance.username = validated_data['username']
        instance.save()
        return instance


