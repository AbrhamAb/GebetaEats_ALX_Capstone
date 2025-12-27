from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from users.permissions import IsCustomer, IsRider, IsVendor

from .models import Delivery, Order
from .serializers import (
    DeliveryAssignSerializer,
    DeliverySerializer,
    DeliveryStatusSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)


def _is_order_owner_or_vendor(user, order: Order) -> bool:
    if not user or not user.is_authenticated:
        return False
    if order.user_id == user.id:
        return True
    vendor_profile = getattr(user, "vendor_profile", None)
    return vendor_profile is not None and order.vendor_id == vendor_profile.id


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        return Order.objects.select_related("vendor", "user").prefetch_related("items__menu_item").filter(user=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsCustomer()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related(
        "vendor", "user").prefetch_related("items__menu_item")
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        order = super().get_object()
        if not _is_order_owner_or_vendor(self.request.user, order):
            raise PermissionDenied("Not allowed to view this order.")
        return order


class VendorOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsVendor]

    def get_queryset(self):
        vendor_profile = getattr(self.request.user, "vendor_profile", None)
        if vendor_profile is None:
            raise PermissionDenied("Vendor profile not found.")
        return Order.objects.select_related("vendor", "user").prefetch_related("items__menu_item").filter(vendor=vendor_profile)


class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related(
        "vendor", "user").prefetch_related("items__menu_item")
    permission_classes = [IsVendor]
    http_method_names = ["patch"]

    def get_object(self):
        order = super().get_object()
        vendor_profile = getattr(self.request.user, "vendor_profile", None)
        if not vendor_profile or order.vendor_id != vendor_profile.id:
            raise PermissionDenied(
                "You can only update orders for your own vendor.")
        return order

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get("status")
        if status_value not in Order.Status.values:
            return Response({"status": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Enforce allowed transitions
        allowed_transitions = {
            Order.Status.PENDING: {Order.Status.ACCEPTED, Order.Status.CANCELLED},
            Order.Status.ACCEPTED: {Order.Status.PREPARING, Order.Status.CANCELLED},
            Order.Status.PREPARING: {Order.Status.OUT_FOR_DELIVERY},
            Order.Status.OUT_FOR_DELIVERY: {Order.Status.DELIVERED},
            Order.Status.DELIVERED: set(),
            Order.Status.CANCELLED: set(),
        }

        current = order.status
        allowed = allowed_transitions.get(current, set())
        if status_value not in allowed:
            return Response({"detail": f"Invalid transition from {current} to {status_value}"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order).data)


class OrderCancelView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related(
        "vendor", "user").prefetch_related("items__menu_item")
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post"]

    def get_object(self):
        order = super().get_object()
        if not _is_order_owner_or_vendor(self.request.user, order):
            raise PermissionDenied("Not allowed to cancel this order.")
        return order

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status not in [Order.Status.PENDING, Order.Status.ACCEPTED]:
            return Response({"detail": "Cannot cancel at this stage."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order).data)


class DeliveryAssignView(generics.UpdateAPIView):
    queryset = Delivery.objects.select_related(
        "order__vendor", "order__user", "rider")
    serializer_class = DeliveryAssignSerializer
    permission_classes = [IsVendor]

    def get_object(self):
        delivery = super().get_object()
        vendor_profile = getattr(self.request.user, "vendor_profile", None)
        if not vendor_profile or delivery.order.vendor != vendor_profile:
            raise PermissionDenied(
                "You can only assign riders for your own orders.")
        return delivery


class DeliveryStatusUpdateView(generics.UpdateAPIView):
    queryset = Delivery.objects.select_related(
        "order__vendor", "order__user", "rider")
    serializer_class = DeliveryStatusSerializer
    permission_classes = [IsRider]

    def get_object(self):
        delivery = super().get_object()
        if delivery.rider != self.request.user:
            raise PermissionDenied(
                "You can only update deliveries assigned to you.")
        return delivery


class RiderAssignedDeliveriesView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [IsRider]

    def get_queryset(self):
        return Delivery.objects.select_related("order__vendor", "order__user").filter(rider=self.request.user)
