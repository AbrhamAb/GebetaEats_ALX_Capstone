from rest_framework import serializers

from .models import Category, MenuItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    vendor_id = serializers.IntegerField(source="vendor.id", read_only=True)
    vendor_name = serializers.CharField(
        source="vendor.restaurant_name", read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "vendor_id",
            "vendor_name",
            "category",
            "name",
            "description",
            "price",
            "photo",
            "is_available",
            "created_at",
            "updated_at",
        ]
