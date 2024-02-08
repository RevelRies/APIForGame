import uuid

from game.models import User

from better_profanity import profanity

profanity.load_censor_words_from_file(filename='./profanity_wordlist.txt')

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenVerifySerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'password', 'email']

        # делаем пароль только для записи чтобы его нельзя было увидеть в ответе API
        # extra_kwargs = {'password': {'write_only': True}}

    def generate_username(self):
        ''' Функция рандомно генерирует username для каждого нового пользователя '''
        return uuid.uuid4()

    def create(self, validated_data):
        ''' Переопределяем метод create для того чтобы пароль сохранялся не в чистом виде, а закодированный '''
        user = User(email=validated_data['email'],
                    username=self.generate_username())
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


