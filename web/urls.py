from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("vendor/<int:vendor_id>/", views.vendor_detail, name="vendor_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("place-order/", views.place_order, name="place_order"),
    path("vendor/dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("rider/dashboard/", views.rider_dashboard, name="rider_dashboard"),
]
