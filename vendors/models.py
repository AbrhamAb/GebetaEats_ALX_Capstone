from django.conf import settings
from django.db import models


class Vendor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vendor_profile")
    restaurant_name = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True)
    is_open = models.BooleanField(default=True)
    location = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.restaurant_name
