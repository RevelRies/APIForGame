from .views import CustomTokenObtainPairView, CustomTokenRefreshView

from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('game/', include('game.urls', namespace='game')),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='apiv1:schema'), name='swagger-ui'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

app_name = 'apiv1'