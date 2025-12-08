from rest_framework import generics, permissions

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
