from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from users.permissions import IsVendor

from .models import Vendor
from .serializers import VendorSerializer


class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.select_related("user").all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]


class VendorDetailView(generics.RetrieveAPIView):
    queryset = Vendor.objects.select_related("user").all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]


class VendorMeView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [IsVendor]

    def get_object(self):
        vendor = getattr(self.request.user, "vendor_profile", None)
        if vendor is None:
            raise PermissionDenied("Vendor profile not found for this user.")
        return vendor
