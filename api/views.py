from rest_framework import viewsets, permissions

from restaurants.models import Restaurant
from menu.models import MenuItem, Category
from orders.models import Order
from restaurants.serializers import RestaurantSerializer
from menu.serializers import MenuItemSerializer, CategorySerializer
from orders.serializers import OrderSerializer


class ReadOnlyOrAuthenticated(permissions.IsAuthenticatedOrReadOnly):
    pass


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrAuthenticated]

    def perform_create(self, serializer):
        # only restaurant users should create menu items
        serializer.save()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_restaurant():
            return Order.objects.filter(items__menu_item__restaurant__owner=user).distinct()
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
