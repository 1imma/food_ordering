from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from menu.models import MenuItem
from .cart import Cart
from .models import Order, OrderItem
from accounts.views import login_required
from decimal import Decimal

# Create your views here.

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = Decimal(0)

    for item_id, item_data in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            quantity = item_data['quantity']
            item_total = menu_item.price * quantity
            total_price += item_total
            cart_items.append({'menu_item': menu_item, 'quantity': quantity, 'total': item_total})
        except MenuItem.DoesNotExist:
            continue

    return render(request, 'orders/cart.html', {'cart_items': cart_items, 'total_price': total_price})



def add_to_cart(request, item_id):
    menu_item = MenuItem.objects.get(id=item_id)

    # Get the cart from session or create an empty one
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        cart[str(item_id)]['quantity'] += 1  # Increase quantity if already in cart
    else:
        cart[str(item_id)] = {'quantity': 1, 'price': str(menu_item.price)}

    request.session['cart'] = cart  # Save cart back to session
    messages.success(request, f"{menu_item.name} added to cart!")

    return redirect('cart')  # Redirect to cart page

def remove_from_cart(request, item_id):
    cart = request.session.get('cart', {})

    if str(item_id) in cart:
        del cart[str(item_id)]  # Remove the item from cart
        request.session['cart'] = cart  # Update session
        messages.success(request, "Item removed from cart.")

    return redirect('cart')  # Redirect back to cart page

def order_success(request):
    return render(request, 'orders/order_success.html')



@login_required
def checkout(request):
    cart = request.session.get('cart', {})  # Get cart from session
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('dashboard')

    total_price = Decimal(0)
    cart_items = []

    for item_id, item_data in cart.items():
        try:
            menu_item = MenuItem.objects.get(id=item_id)
            quantity = item_data['quantity']
            item_total = menu_item.price * quantity
            total_price += item_total
            cart_items.append({'menu_item': menu_item, 'quantity': quantity, 'total': item_total})
        except MenuItem.DoesNotExist:
            continue  # Skip items that no longer exist

    if request.method == 'POST':
        # Create an order
        order = Order.objects.create(user=request.user, total_price=total_price)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                menu_item=item['menu_item'],
                quantity=item['quantity'],
                price=item['menu_item'].price
            )

        # Clear the cart session
        request.session['cart'] = {}

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')

    return render(request, 'orders/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def order_tracking(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in!")
        return redirect('login')

    user_id = request.session['user_id']
    orders = Order.objects.filter(user_id=user_id).order_by('-created_at')

    return render(request, 'orders/order_tracking.html', {'orders': orders})

