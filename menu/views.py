from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from users.permissions import IsVendor, IsVendorOwner

from .models import MenuItem
from .serializers import MenuItemSerializer


class MenuItemListView(generics.ListAPIView):
    queryset = MenuItem.objects.select_related("vendor", "category").all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        vendor_id = self.request.query_params.get("vendor")
        category_id = self.request.query_params.get("category")
        available = self.request.query_params.get("available")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if vendor_id:
            qs = qs.filter(vendor_id=vendor_id)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if available is not None:
            flag = available.lower()
            if flag in ("true", "1", "yes"):
                qs = qs.filter(is_available=True)
            elif flag in ("false", "0", "no"):
                qs = qs.filter(is_available=False)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        return qs


class MenuItemDetailView(generics.RetrieveAPIView):
    queryset = MenuItem.objects.select_related("vendor", "category").all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]


class VendorMenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsVendor()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        vendor_id = self.kwargs.get("vendor_id")
        return MenuItem.objects.select_related("vendor", "category").filter(vendor_id=vendor_id)

    def perform_create(self, serializer):
        vendor_id = self.kwargs.get("vendor_id")
        vendor_profile = getattr(self.request.user, "vendor_profile", None)
        if vendor_profile is None or vendor_profile.id != vendor_id:
            raise PermissionDenied(
                "You can only create menu items for your own vendor profile.")
        serializer.save(vendor=vendor_profile)


class VendorMenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.select_related("vendor", "category")

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [IsVendor(), IsVendorOwner()]

    def get_queryset(self):
        vendor_id = self.kwargs.get("vendor_id")
        return MenuItem.objects.select_related("vendor", "category").filter(vendor_id=vendor_id)
