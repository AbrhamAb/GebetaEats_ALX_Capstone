from django.urls import path

from .views import VendorMenuListView

urlpatterns = [
    path("<int:vendor_id>/menu/", VendorMenuListView.as_view(), name="vendor-menu"),
]
