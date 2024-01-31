from django.urls import path, re_path, include
from .views import SingUpView, GoogleAuthView

urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    path('oauth/complete/google-auth/', GoogleAuthView.as_view(), name='google-auth'),
    path('oauth/', include('social_django.urls', namespace='apiv1:accounts:social'))
]

app_name = 'accounts'


# /oauth/login/google-oauth2/