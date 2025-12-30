from decimal import Decimal

from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Delivery, Order, OrderItem
from menu.models import MenuItem
from menu.serializers import MenuItemSerializer
from accounts.serializers import UserSerializer
from restaurants.serializers import RestaurantSerializer


User = get_user_model()


class OrderItemCreateSerializer(serializers.Serializer):
    menu_item = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
    delivery_address = serializers.CharField()

    def validate(self, attrs):
        items = attrs.get("items", [])
        if not items:
            raise serializers.ValidationError("At least one item is required.")
        first_rest = items[0]["menu_item"].restaurant
        for it in items:
            if it["menu_item"].restaurant != first_rest:
                raise serializers.ValidationError(
                    "All items must be from the same restaurant.")
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        items = validated_data.pop("items")
        delivery_address = validated_data.get("delivery_address")
        restaurant = items[0]["menu_item"].restaurant

        order = Order.objects.create(
            user=user, restaurant=restaurant, delivery_address=delivery_address)
        total = Decimal("0.00")
        order_items = []
        for it in items:
            menu_item = it["menu_item"]
            qty = it["quantity"]
            unit = menu_item.price
            line = unit * qty
            order_items.append(OrderItem(
                order=order, menu_item=menu_item, quantity=qty, unit_price=unit, line_total=line))
            total += line
        OrderItem.objects.bulk_create(order_items)
        order.total_price = total
        order.save()
        Delivery.objects.create(order=order)
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity", "unit_price", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "restaurant", "status", "delivery_address",
                  "total_price", "items", "created_at", "updated_at"]


class DeliverySerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = ["id", "order", "rider", "status", "notes",
                  "assigned_at", "picked_at", "delivered_at", "updated_at"]
        read_only_fields = ["order", "updated_at",
                            "assigned_at", "picked_at", "delivered_at"]


class DeliveryAssignSerializer(serializers.ModelSerializer):
    rider_id = serializers.PrimaryKeyRelatedField(
        source="rider", queryset=User.objects.all(), required=True)

    class Meta:
        model = Delivery
        fields = ["rider_id", "status", "notes"]

    def validate(self, attrs):
        attrs.setdefault("status", Delivery.Status.ASSIGNED)
        return attrs


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ["status", "notes"]
