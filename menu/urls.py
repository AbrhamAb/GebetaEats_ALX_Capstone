from django.urls import path
from .views import CategoryListView, MenuItemListCreateView, MenuItemDetailView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("items/", MenuItemListCreateView.as_view(), name="menuitem-list"),
    path("items/<int:pk>/", MenuItemDetailView.as_view(), name="menuitem-detail"),
]
