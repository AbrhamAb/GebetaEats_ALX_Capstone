from django.contrib import admin

from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "location", "thumbnail")
    search_fields = ("name", "owner__username")

    def thumbnail(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;" />', obj.image.url)
        return ""

    thumbnail.short_description = "Image"
