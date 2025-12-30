from django.urls import path
from .views import (
    DeliveryAssignView,
    DeliveryStatusUpdateView,
    OrderCancelView,
    OrderDetailView,
    OrderListCreateView,
    OrderStatusUpdateView,
    RiderAssignedDeliveriesView,
    RestaurantOrderListView,
)

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("<int:pk>/status/", OrderStatusUpdateView.as_view(), name="order-status"),
    path("<int:pk>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
    path("restaurant/", RestaurantOrderListView.as_view(),
         name="restaurant-order-list"),
    path("delivery/<int:pk>/assign/",
         DeliveryAssignView.as_view(), name="delivery-assign"),
    path("delivery/<int:pk>/status/",
         DeliveryStatusUpdateView.as_view(), name="delivery-status"),
    path("delivery/assigned/", RiderAssignedDeliveriesView.as_view(),
         name="delivery-assigned"),
]
