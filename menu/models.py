from django.db import models

from vendors.models import Vendor


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class MenuItem(models.Model):
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="menu_items")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="menu_items", blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.CharField(max_length=255, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name
