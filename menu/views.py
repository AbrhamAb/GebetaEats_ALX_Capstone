from rest_framework import generics, permissions

from .models import MenuItem
from .serializers import MenuItemSerializer


class VendorMenuListView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        vendor_id = self.kwargs.get("vendor_id")
        return MenuItem.objects.select_related("vendor", "category").filter(vendor_id=vendor_id)
