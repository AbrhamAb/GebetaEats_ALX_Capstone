from django.urls import path

from .views import VendorDetailView, VendorListView

urlpatterns = [
    path("", VendorListView.as_view(), name="vendor-list"),
    path("<int:pk>/", VendorDetailView.as_view(), name="vendor-detail"),
]
