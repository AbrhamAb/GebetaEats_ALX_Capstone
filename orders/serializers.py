from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from menu.serializers import MenuItemSerializer
from menu.models import MenuItem
from users.serializers import UserSerializer
from vendors.serializers import VendorSerializer

from .models import Delivery, Order, OrderItem

User = get_user_model()


class OrderItemCreateSerializer(serializers.Serializer):
    menu_item_id = serializers.PrimaryKeyRelatedField(
        source="menu_item", queryset=MenuItem.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity", "unit_price", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    vendor = VendorSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "vendor",
            "status",
            "delivery_address",
            "total_price",
            "items",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)
    delivery_address = serializers.CharField()

    def validate(self, attrs):
        items = attrs.get("items", [])
        if not items:
            raise serializers.ValidationError(
                "At least one item is required to create an order.")

        first_vendor = items[0]["menu_item"].vendor
        for item in items:
            if item["menu_item"].vendor != first_vendor:
                raise serializers.ValidationError(
                    "All items in an order must belong to the same vendor.")
        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        items = validated_data.pop("items")
        delivery_address = validated_data.get("delivery_address")
        vendor = items[0]["menu_item"].vendor

        order = Order.objects.create(
            user=user,
            vendor=vendor,
            status=Order.Status.PENDING,
            delivery_address=delivery_address,
        )
        total = Decimal("0")
        order_items = []
        for item in items:
            menu_item: MenuItem = item["menu_item"]
            quantity = item["quantity"]
            unit_price = menu_item.price
            line_total = unit_price * quantity
            total += line_total
            order_items.append(
                OrderItem(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                )
            )
        OrderItem.objects.bulk_create(order_items)
        order.total_price = total
        order.save(update_fields=["total_price"])
        Delivery.objects.create(order=order)
        return order


class DeliverySerializer(serializers.ModelSerializer):
    rider = UserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = [
            "id",
            "order",
            "rider",
            "status",
            "notes",
            "assigned_at",
            "picked_at",
            "delivered_at",
            "updated_at",
        ]
        read_only_fields = ["order", "updated_at",
                            "assigned_at", "picked_at", "delivered_at"]


class DeliveryAssignSerializer(serializers.ModelSerializer):
    rider_id = serializers.PrimaryKeyRelatedField(
        source="rider", queryset=User.objects.filter(role="rider"), required=True
    )

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
