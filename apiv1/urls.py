from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('gameprocess/', include('gameprocess.urls', namespace='gameprocess')),
]
