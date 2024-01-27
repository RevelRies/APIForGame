from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('gameprocess/', include('gameprocess.urls', namespace='gameprocess')),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='apiv1:schema'), name='swagger-ui'),
]

app_name = 'apiv1'