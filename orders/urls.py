from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, checkout, order_success,order_tracking

urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-success/', order_success, name='order_success'),
    path('order-tracking/', order_tracking, name='order_tracking'),
]