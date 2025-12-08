from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Vendor

User = get_user_model()


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "role"]


class VendorSerializer(serializers.ModelSerializer):
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = [
            "id",
            "user",
            "restaurant_name",
            "logo",
            "is_open",
            "location",
            "rating",
            "created_at",
            "updated_at",
        ]
