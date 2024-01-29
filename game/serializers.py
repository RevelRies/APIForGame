from .models import User
from rest_framework.serializers import ModelSerializer


class UserDataSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'all_time_score', 'all_time_high_score', 'coins']


class UserSaveCoinsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'coins']

    def update(self, instance, validated_data):
        # instanse - это объект User
        instance.coins += validated_data['coins']
        instance.save()
        return instance