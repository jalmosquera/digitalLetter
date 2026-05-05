
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from core.views import health_check

_docs_permissions = [AllowAny] if settings.DEBUG else [IsAuthenticated]

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=_docs_permissions), name='schema'),
    path('', SpectacularRedocView.as_view(url_name='schema', permission_classes=_docs_permissions), name='redoc'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=_docs_permissions), name='swagger-ui'),

    # Auth - Uses username for authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Categories API
    path('api/', include('apps.categories.api.router')),  # Categories API

    # Ingredients API
    path('api/', include('apps.ingredients.api.router')),  # Ingredients API

    # Products API
    path('api/', include('apps.products.api.router')),  # Products API

    # Company API
    path('api/', include('apps.company.api.router')),  # Company API
    # Users API
    path('api/', include('apps.users.api.router')),  # Users API
    # Orders API
    path('api/orders/', include('apps.orders.api.router')),  # Orders API

    # Promotions API
    path('api/', include('apps.promotions.api.router')),  # Promotions API


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
