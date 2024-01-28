from django.urls import path
from .views import SingUpView, UserDataView

urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    path('userdata/', UserDataView.as_view(), name='userdata'),
]

app_name = 'accounts'