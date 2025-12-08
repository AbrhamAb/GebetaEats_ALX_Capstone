from django.contrib import admin

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("id", "restaurant_name", "is_open", "rating")
    search_fields = ("restaurant_name", "location")
