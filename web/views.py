from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from menu.models import MenuItem
from restaurants.models import Restaurant
from orders.models import Order, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from accounts.forms import RegisterForm
from restaurants.forms import RestaurantForm
from menu.forms import MenuItemForm
from menu.models import MenuItem, Category


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'web/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'web/login.html', {'error': 'Invalid credentials'})
    return render(request, 'web/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'web/home.html', {'restaurants': restaurants})


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.menu_items.filter(is_available=True)
    return render(request, 'web/restaurant_detail.html', {'restaurant': restaurant, 'items': items})


def _get_cart(session):
    return session.setdefault('cart', {})


@require_POST
def add_to_cart(request):
    item_id = request.POST.get('item_id')
    qty = int(request.POST.get('quantity', 1))
    item = get_object_or_404(MenuItem, pk=item_id)
    cart = _get_cart(request.session)
    cart_item = cart.get(str(item_id), {'quantity': 0})
    cart_item['quantity'] = cart_item.get('quantity', 0) + qty
    cart_item['price'] = str(item.price)
    cart[str(item_id)] = cart_item
    request.session.modified = True
    # If this is an AJAX request, return JSON with updated cart count
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax:
        count = sum(int(v.get('quantity', 0)) for v in cart.values())
        return JsonResponse({
            'success': True,
            'count': count,
            'message': f'Added {item.name} to cart',
            'cart_preview_url': reverse('cart_preview')
        })
    return redirect('cart')


@require_POST
def update_cart(request):
    # expects pairs of item_id and quantity
    cart = _get_cart(request.session)
    for key, val in request.POST.items():
        if key.startswith('qty_'):
            item_id = key.split('qty_')[1]
            try:
                q = int(val)
            except Exception:
                q = 0
            if q <= 0:
                cart.pop(item_id, None)
            else:
                if item_id in cart:
                    cart[item_id]['quantity'] = q
    request.session.modified = True
    return redirect('cart')


def cart_view(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal('0.00')
    for item_id, data in cart.items():
        try:
            menu_item = MenuItem.objects.get(pk=int(item_id))
        except MenuItem.DoesNotExist:
            continue
        qty = data.get('quantity', 0)
        line = menu_item.price * qty
        items.append(
            {'menu_item': menu_item, 'quantity': qty, 'line_total': line})
        total += line
    return render(request, 'web/cart.html', {'items': items, 'total': total})


def cart_count(request):
    cart = _get_cart(request.session)
    count = sum(int(v.get('quantity', 0)) for v in cart.values())
    return JsonResponse({'count': count})


def cart_preview(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal('0.00')
    for item_id, data in cart.items():
        try:
            menu_item = MenuItem.objects.get(pk=int(item_id))
        except MenuItem.DoesNotExist:
            continue
        qty = int(data.get('quantity', 0))
        line = menu_item.price * qty
        items.append({
            'id': menu_item.id,
            'name': menu_item.name,
            'quantity': qty,
            'line_total': str(line),
            'url': reverse('restaurant_detail', args=[menu_item.restaurant.id])
        })
        total += line
    return JsonResponse({'items': items, 'total': str(total)})


@login_required
def checkout(request):
    cart = _get_cart(request.session)
    if not cart:
        return redirect('home')
    if request.method == 'POST':
        address = request.POST.get('address', '')
        # Determine restaurant for the order — cart must contain items from a single restaurant
        restaurants_in_cart = set()
        for item_id in cart.keys():
            try:
                mi = MenuItem.objects.get(pk=int(item_id))
            except MenuItem.DoesNotExist:
                continue
            if mi.restaurant:
                restaurants_in_cart.add(mi.restaurant)

        if not restaurants_in_cart:
            return redirect('cart')
        if len(restaurants_in_cart) > 1:
            # Simple handling: do not allow multi-restaurant orders from the cart
            return render(request, 'web/checkout.html', {'error': 'Your cart contains items from multiple restaurants. Please order from one restaurant at a time.'})

        restaurant = restaurants_in_cart.pop()

        order = Order.objects.create(
            user=request.user, restaurant=restaurant, delivery_address=address)
        total = Decimal('0.00')
        for item_id, data in cart.items():
            menu_item = MenuItem.objects.get(pk=int(item_id))
            qty = data.get('quantity', 0)
            unit = menu_item.price
            line = unit * qty
            OrderItem.objects.create(
                order=order, menu_item=menu_item, quantity=qty, unit_price=unit, line_total=line)
            total += line
        order.total_price = total
        order.save()
        # clear cart
        request.session['cart'] = {}
        request.session.modified = True
        return redirect('order_success', pk=order.pk)
    # GET shows a simple checkout form
    return render(request, 'web/checkout.html')


def order_success(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'web/order_success.html', {'order': order})


@login_required
def restaurant_orders(request):
    # owner view for orders belonging to their restaurant
    user = request.user
    if not user.is_restaurant():
        return redirect('home')
    orders = Order.objects.filter(
        items__menu_item__restaurant__owner=user).distinct()
    return render(request, 'web/restaurant_orders.html', {'orders': orders, 'status_choices': Order.Status.choices})


@login_required
def restaurant_update_order(request, pk):
    user = request.user
    if not user.is_restaurant():
        return redirect('home')
    order = get_object_or_404(Order, pk=pk)
    if not order.items.filter(menu_item__restaurant__owner=user).exists():
        return redirect('restaurant_orders')
    if request.method == 'POST':
        status = request.POST.get('status')
        valid_statuses = [s.value for s in Order.Status]
        if status in valid_statuses:
            order.status = status
            order.save()
    return redirect('restaurant_orders')


@login_required
def my_orders(request):
    # list orders for the logged-in customer
    user = request.user
    orders = Order.objects.filter(
        user=user).prefetch_related('items__menu_item')
    return render(request, 'web/my_orders.html', {'orders': orders})


@login_required
def owner_dashboard(request):
    user = request.user
    if not getattr(user, 'is_restaurant', lambda: False)():
        return redirect('home')
    restaurant = Restaurant.objects.filter(owner=user).first()
    orders = Order.objects.filter(restaurant__owner=user).prefetch_related(
        'items__menu_item') if restaurant else []
    return render(request, 'web/owner/dashboard.html', {'restaurant': restaurant, 'orders': orders})


@login_required
def manage_restaurant(request):
    user = request.user
    if not getattr(user, 'is_restaurant', lambda: False)():
        return redirect('home')
    restaurant = Restaurant.objects.filter(owner=user).first()
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            r = form.save(commit=False)
            r.owner = user
            r.save()
            return redirect('owner_dashboard')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'web/owner/restaurant_form.html', {'form': form, 'restaurant': restaurant})


@login_required
def owner_menu_list(request):
    user = request.user
    if not getattr(user, 'is_restaurant', lambda: False)():
        return redirect('home')
    restaurant = Restaurant.objects.filter(owner=user).first()
    if not restaurant:
        return redirect('owner_restaurant')
    items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'web/owner/menu_list.html', {'items': items, 'restaurant': restaurant})


@login_required
def owner_menu_add(request):
    user = request.user
    if not getattr(user, 'is_restaurant', lambda: False)():
        return redirect('home')
    restaurant = Restaurant.objects.filter(owner=user).first()
    if not restaurant:
        return redirect('owner_restaurant')
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            mi = form.save(commit=False)
            mi.restaurant = restaurant
            mi.save()
            return redirect('owner_menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'web/owner/menu_form.html', {'form': form, 'restaurant': restaurant})


@login_required
def owner_menu_edit(request, pk):
    user = request.user
    if not getattr(user, 'is_restaurant', lambda: False)():
        return redirect('home')
    restaurant = Restaurant.objects.filter(owner=user).first()
    if not restaurant:
        return redirect('owner_restaurant')
    menu_item = get_object_or_404(MenuItem, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('owner_menu_list')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'web/owner/menu_form.html', {'form': form, 'restaurant': restaurant, 'menu_item': menu_item})


@login_required
def owner_menu_delete(request, pk):
    user = request.user
    if not getattr(user, 'is_restaurant', lambda: False)():
        return redirect('home')
    restaurant = Restaurant.objects.filter(owner=user).first()
    if not restaurant:
        return redirect('owner_restaurant')
    menu_item = get_object_or_404(MenuItem, pk=pk, restaurant=restaurant)
    if request.method == 'POST':
        menu_item.delete()
        return redirect('owner_menu_list')
    return render(request, 'web/owner/menu_confirm_delete.html', {'menu_item': menu_item, 'restaurant': restaurant})
