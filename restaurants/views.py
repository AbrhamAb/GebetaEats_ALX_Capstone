from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_authenticated or not getattr(user, 'is_restaurant', lambda: False)():
            raise PermissionDenied(
                'Only restaurant users may create a restaurant profile')
        serializer.save(owner=user)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def perform_update(self, serializer):
        instance = self.get_object()
        if self.request.user != instance.owner:
            raise PermissionDenied('Only the owner may update this restaurant')
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionDenied('Only the owner may delete this restaurant')
        instance.delete()
