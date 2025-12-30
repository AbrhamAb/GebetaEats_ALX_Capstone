from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('restaurant/<int:pk>/', views.restaurant_detail, name='restaurant_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/count/', views.cart_count, name='cart_count'),
    path('cart/preview/', views.cart_preview, name='cart_preview'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:pk>/', views.order_success, name='order_success'),
    path('restaurant/orders/', views.restaurant_orders, name='restaurant_orders'),
    path('restaurant/order/<int:pk>/update/',
         views.restaurant_update_order, name='restaurant_update_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    # owner dashboard and restaurant management
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('owner/restaurant/', views.manage_restaurant, name='owner_restaurant'),
    # owner menu management
    path('owner/menu/', views.owner_menu_list, name='owner_menu_list'),
    path('owner/menu/add/', views.owner_menu_add, name='owner_menu_add'),
    path('owner/menu/<int:pk>/edit/',
         views.owner_menu_edit, name='owner_menu_edit'),
    path('owner/menu/<int:pk>/delete/',
         views.owner_menu_delete, name='owner_menu_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
