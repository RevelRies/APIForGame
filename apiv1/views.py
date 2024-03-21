from game.models import User

from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Выполняем стандартную логику получения токенов
        response = super().post(request, *args, **kwargs)

        # Записываю действующий refresh token в модель пользователя
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            user_refresh_token = user.refresh_token

            # если у пользователя есть на данный момент refresh token, то мы его добавляем в черный список
            if user_refresh_token != 'None':

                # если токен не истек - добавляем его в черный список
                try:
                    token = RefreshToken(user_refresh_token)
                    token.blacklist()
                # если истек - ничего не делаем
                except:
                    pass

            user.refresh_token = response.data.get('refresh')
            user.save()
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Выполняем стандартную логику получения токенов
        response = super().post(request, *args, **kwargs)

        try:
            # получаю id пользователя из токена и записываю ему в поле действующий токен
            token = RefreshToken(response.data.get('refresh'))
            user = User.objects.get(pk=token.get('user_id'))
            user.refresh_token = response.data.get('refresh')
            user.save()
        except Exception as ex:
            return Response({"error": f"{ex}"}, status=status.HTTP_400_BAD_REQUEST)

        return response