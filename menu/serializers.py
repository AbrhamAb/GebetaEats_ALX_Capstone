from rest_framework import serializers

from .models import Category, MenuItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.ReadOnlyField(source='restaurant.id')

    class Meta:
        model = MenuItem
        fields = ("id", "restaurant", "category", "name",
                  "description", "price", "image", "is_available")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source="category", queryset=Category.objects.all(), write_only=True, required=False, allow_null=True
    )
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
            "category_id",
            "name",
            "description",
            "price",
            "photo",
            "is_available",
            "created_at",
            "updated_at",
        ]
