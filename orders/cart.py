class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, menu_item, quantity=1):
        menu_item_id = str(menu_item.id)

        if menu_item_id in self.cart:
            self.cart[menu_item_id]['quantity'] += quantity
        else:
            self.cart[menu_item_id] = {
                'name': menu_item.name,
                'price': str(menu_item.price),
                'quantity': quantity,
            }

        self.save()

    def remove(self, menu_item_id):
        if str(menu_item_id) in self.cart:
            del self.cart[str(menu_item_id)]
            self.save()

    def save(self):
        self.session.modified = True

    def get_total_price(self):
        return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True
