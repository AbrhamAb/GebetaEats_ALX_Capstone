from django.contrib import admin

from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "price", "is_available", "thumbnail")
    list_filter = ("is_available", "category")
    search_fields = ("name", "restaurant__name")

    def thumbnail(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;" />', obj.image.url)
        return ""

    thumbnail.short_description = "Image"
