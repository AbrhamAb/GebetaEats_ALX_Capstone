from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import RestaurantViewSet, MenuItemViewSet, CategoryViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'items', MenuItemViewSet, basename='menuitem')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
