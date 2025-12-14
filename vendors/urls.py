from django.urls import path

from .views import VendorDetailView, VendorListView, VendorMeView

urlpatterns = [
    path("", VendorListView.as_view(), name="vendor-list"),
    path("me/", VendorMeView.as_view(), name="vendor-me"),
    path("<int:pk>/", VendorDetailView.as_view(), name="vendor-detail"),
]
