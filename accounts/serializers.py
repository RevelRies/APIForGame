import uuid

from game.models import User
from rest_framework.serializers import ModelSerializer


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


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'all_time_score', 'all_time_high_score', 'coins']