from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ("menu_item", "quantity", "unit_price", "line_total")
    readonly_fields = ("unit_price", "line_total")
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "status",
                    "delivery_address", "total_price", "created_at", "updated_at")
    list_filter = ("status", "restaurant")
    search_fields = ("user__username", "restaurant__name", "delivery_address")
    readonly_fields = ("total_price", "created_at", "updated_at")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)


class DeliveryInline(admin.StackedInline):
    from .models import Delivery

    model = Delivery
    readonly_fields = ("assigned_at", "picked_at",
                       "delivered_at", "updated_at")
    can_delete = False
    max_num = 1

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(OrderItem)
try:
    from .models import Delivery
    admin.site.register(Delivery)
except Exception:
    pass
