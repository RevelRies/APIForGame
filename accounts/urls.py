from django.urls import path, re_path, include
from .views import SingUpView

urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    re_path(r'^oauth/', include('social_django.urls', namespace='apiv1:accounts:social'))
]

app_name = 'accounts'


# /oauth/login/google-oauth2/