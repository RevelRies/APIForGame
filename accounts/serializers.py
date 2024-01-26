from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    # def validate(self, data):
    #     email = data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise serializers.ValidationError({"email": "This email is already taken."})
    #     return data