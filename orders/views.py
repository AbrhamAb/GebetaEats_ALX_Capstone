from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .serializers import (
    DeliveryAssignSerializer,
    DeliverySerializer,
    DeliveryStatusSerializer,
    OrderCreateSerializer,
    OrderSerializer,
)
from .models import Delivery, Order


def _is_order_owner_or_restaurant(user, order: Order) -> bool:
    if not user or not user.is_authenticated:
        return False
    if order.user_id == user.id:
        return True
    # restaurant owners: check if user's restaurant matches order.restaurant
    if getattr(user, 'is_restaurant', lambda: False)():
        if hasattr(user, 'restaurant') and order.restaurant_id == user.restaurant.id:
            return True
    return False


class OrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'is_restaurant', lambda: False)():
            return Order.objects.filter(restaurant__owner=user).prefetch_related('items__menu_item')
        return Order.objects.filter(user=user).prefetch_related('items__menu_item')

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related(
        'restaurant', 'user').prefetch_related('items__menu_item')
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        order = super().get_object()
        if not _is_order_owner_or_restaurant(self.request.user, order):
            raise PermissionDenied("Not allowed to view this order.")
        return order


class RestaurantOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not getattr(user, 'is_restaurant', lambda: False)():
            raise PermissionDenied(
                "Only restaurant users may view these orders.")
        return Order.objects.filter(restaurant__owner=user).prefetch_related('items__menu_item')


class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related(
        'restaurant', 'user').prefetch_related('items__menu_item')
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch"]

    def get_object(self):
        order = super().get_object()
        user = self.request.user
        if not getattr(user, 'is_restaurant', lambda: False)():
            raise PermissionDenied("Only restaurant users may update status.")
        if not hasattr(user, 'restaurant') or order.restaurant_id != user.restaurant.id:
            raise PermissionDenied(
                "You can only update orders for your own restaurant.")
        return order

    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        status_value = request.data.get("status")
        if status_value not in [s.value for s in Order.Status]:
            return Response({"status": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        allowed_transitions = {
            Order.Status.PENDING: {Order.Status.PREPARING, Order.Status.CANCELLED},
            Order.Status.PREPARING: {Order.Status.OUT_FOR_DELIVERY},
            Order.Status.OUT_FOR_DELIVERY: {Order.Status.DELIVERED},
            Order.Status.DELIVERED: set(),
            Order.Status.CANCELLED: set(),
        }

        current = order.status
        allowed = allowed_transitions.get(current, set())
        # map enum members to values
        allowed_values = {a.value for a in allowed}
        if status_value not in allowed_values:
            return Response({"detail": f"Invalid transition from {current} to {status_value}"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_value
        order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order).data)


class OrderCancelView(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.select_related(
        'restaurant', 'user').prefetch_related('items__menu_item')
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["post"]

    def get_object(self):
        order = super().get_object()
        if not _is_order_owner_or_restaurant(self.request.user, order):
            raise PermissionDenied("Not allowed to cancel this order.")
        return order

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status not in [Order.Status.PENDING, Order.Status.PREPARING]:
            return Response({"detail": "Cannot cancel at this stage."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order).data)


class DeliveryAssignView(generics.UpdateAPIView):
    queryset = Delivery.objects.select_related(
        'order__restaurant', 'order__user', 'rider')
    serializer_class = DeliveryAssignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        delivery = super().get_object()
        user = self.request.user
        if not getattr(user, 'is_restaurant', lambda: False)():
            raise PermissionDenied(
                "Only restaurant users may assign deliveries.")
        if not hasattr(user, 'restaurant') or delivery.order.restaurant_id != user.restaurant.id:
            raise PermissionDenied(
                "You can only assign deliveries for your own restaurant orders.")
        return delivery


class DeliveryStatusUpdateView(generics.UpdateAPIView):
    queryset = Delivery.objects.select_related(
        'order__restaurant', 'order__user', 'rider')
    serializer_class = DeliveryStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        delivery = super().get_object()
        if delivery.rider != self.request.user:
            raise PermissionDenied(
                "You can only update deliveries assigned to you.")
        return delivery


class RiderAssignedDeliveriesView(generics.ListAPIView):
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Delivery.objects.select_related('order__restaurant', 'order__user').filter(rider=self.request.user)
