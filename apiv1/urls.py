from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('game/', include('game.urls', namespace='game')),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='apiv1:schema'), name='swagger-ui'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

app_name = 'apiv1'