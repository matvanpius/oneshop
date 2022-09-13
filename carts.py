import decimal

from itertools import product
from django.conf import settings
from myApp.web.models import Product
from .views import cart
from django.shortcuts import redirect, render, get_object_or_404


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

def cart_add(request,product_id):
    cart = Cart(request)
    product_id = get_objects_or_404(Product,id=product_id)
    form = CartAddForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'])
        return redirect('cart')


def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    

        for item in self.cart.values():
            item['price'] = decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

def get_total_price(self):
        return sum((item['price']) * item['quantity'] for item in self.cart.values())

def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True