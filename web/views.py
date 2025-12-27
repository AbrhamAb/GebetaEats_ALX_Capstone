from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from menu.models import MenuItem
from vendors.models import Vendor
from orders.models import Delivery, Order, OrderItem


def index(request):
    vendors = Vendor.objects.all()
    return render(request, "web/index.html", {"vendors": vendors})


def vendor_detail(request, vendor_id: int):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    menu_items = vendor.menu_items.filter(is_available=True)

    if request.method == "POST":
        # add to session cart
        menu_item_id = int(request.POST.get("menu_item_id"))
        quantity = int(request.POST.get("quantity", 1))
        menu_item = get_object_or_404(MenuItem, pk=menu_item_id, vendor=vendor)

        cart = request.session.get("cart") or {
            "vendor_id": vendor_id, "items": []}
        # if different vendor, reset cart
        if cart.get("vendor_id") != vendor_id:
            cart = {"vendor_id": vendor_id, "items": []}

        # append or update existing
        found = None
        for it in cart["items"]:
            if int(it["menu_item_id"]) == menu_item.id:
                it["quantity"] = int(it["quantity"]) + quantity
                it["line_total"] = float(
                    Decimal(it["quantity"]) * menu_item.price)
                found = it
                break
        if not found:
            cart["items"].append({
                "menu_item_id": menu_item.id,
                "name": menu_item.name,
                "unit_price": float(menu_item.price),
                "quantity": quantity,
                "line_total": float(menu_item.price * quantity),
            })

        # compute total
        total = Decimal("0")
        for it in cart["items"]:
            total += Decimal(str(it["line_total"]))
        cart["total"] = float(total)
        request.session["cart"] = cart
        return redirect("web:cart")

    return render(request, "web/vendor_detail.html", {"vendor": vendor, "menu_items": menu_items})


def cart_view(request):
    cart = request.session.get("cart") or {"items": [], "total": 0}
    return render(request, "web/cart.html", {"cart": cart})


@login_required
@require_POST
def place_order(request):
    user = request.user
    if user.role != "user":
        return render(request, "web/order_error.html", {"message": "Only customers can place orders."})

    cart = request.session.get("cart")
    if not cart or not cart.get("items"):
        return render(request, "web/order_error.html", {"message": "Cart is empty."})

    vendor = get_object_or_404(Vendor, pk=cart["vendor_id"])
    delivery_address = request.POST.get("delivery_address", user.address or "")

    order = Order.objects.create(user=user, vendor=vendor, status=Order.Status.PENDING,
                                 delivery_address=delivery_address, total_price=Decimal("0"))
    total = Decimal("0")
    for it in cart["items"]:
        menu_item = get_object_or_404(MenuItem, pk=it["menu_item_id"])
        quantity = int(it["quantity"])
        unit_price = Decimal(str(it["unit_price"]))
        line_total = unit_price * quantity
        OrderItem.objects.create(order=order, menu_item=menu_item,
                                 quantity=quantity, unit_price=unit_price, line_total=line_total)
        total += line_total

    order.total_price = total
    order.save(update_fields=["total_price"])
    Delivery.objects.create(order=order)
    # clear cart
    request.session.pop("cart", None)
    return render(request, "web/order_success.html", {"order": order})


def vendor_dashboard(request):
    if not request.user.is_authenticated or request.user.role != "vendor":
        return redirect("web:index")
    vendor = getattr(request.user, "vendor_profile", None)
    if vendor is None:
        return render(request, "web/order_error.html", {"message": "Vendor profile not found."})
    orders = Order.objects.filter(vendor=vendor).select_related(
        "user").prefetch_related("items__menu_item")
    return render(request, "web/vendor_dashboard.html", {"orders": orders, "vendor": vendor})


def rider_dashboard(request):
    if not request.user.is_authenticated or request.user.role != "rider":
        return redirect("web:index")
    deliveries = Delivery.objects.filter(
        rider=request.user).select_related("order__vendor", "order__user")
    return render(request, "web/rider_dashboard.html", {"deliveries": deliveries})
