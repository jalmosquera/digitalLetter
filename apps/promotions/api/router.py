"""URL router for Promotions API."""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.promotions.api.views import PromotionViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'promotions', PromotionViewSet, basename='promotion')

# URL patterns
urlpatterns = router.urls
