from django.urls import path

from .views import (
    MenuItemDetailView,
    MenuItemListView,
    VendorMenuDetailView,
    VendorMenuListCreateView,
)

urlpatterns = [
    path("menu-items/", MenuItemListView.as_view(), name="menuitem-list"),
    path("menu-items/<int:pk>/", MenuItemDetailView.as_view(),
         name="menuitem-detail"),
    path("<int:vendor_id>/menu/",
         VendorMenuListCreateView.as_view(), name="vendor-menu"),
    path(
        "<int:vendor_id>/menu/<int:pk>/",
        VendorMenuDetailView.as_view(),
        name="vendor-menu-detail",
    ),
]
