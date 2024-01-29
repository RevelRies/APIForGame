from django.urls import path, re_path, include
from .views import SingUpView, UserDataView

urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    path('userdata/', UserDataView.as_view(), name='userdata'),
    re_path(r'^oauth/', include('social_django.urls', namespace='apiv1:accounts:social'))
]

app_name = 'accounts'


# /oauth/login/google-oauth2/