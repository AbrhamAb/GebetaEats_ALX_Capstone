from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        restaurant_id = self.request.data.get('restaurant')
        # Ensure only the restaurant owner can create items for their restaurant
        if not user.is_authenticated or not user.is_restaurant():
            raise PermissionDenied(
                'Only restaurant users may create menu items')
        # assign restaurant matching the owner
        from restaurants.models import Restaurant

        try:
            rest = Restaurant.objects.get(id=restaurant_id)
        except Exception:
            raise PermissionDenied('Invalid restaurant')
        if rest.owner != user:
            raise PermissionDenied('You do not own this restaurant')
        serializer.save(restaurant=rest)


class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user != instance.restaurant.owner:
            raise PermissionDenied('Only the owner may update this menu item')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.restaurant.owner:
            raise PermissionDenied('Only the owner may delete this menu item')
        instance.delete()
