# product/utils.py
from email.policy import default
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from accounts.models import InventoryItem, Address
from product.models import Product, Variation
from payment.models import Order, OrderItem, InfosForm
from cart.models import Cart
import stripe
from django.conf import settings

stripe.api_key = settings.API_STRIPE

def create_order(metadata, items):
    user = User.objects.get(id=metadata["user_id"])
    price = items[0]["price_data"]["unit_amount"] / 100
    address = Address.objects.get(id=metadata["address"])
    infos_form = InfosForm.objects.create(
        user = user,
        address = address.address,
        complement = address.complement,
        neighborhood = address.neighborhood,
        number = address.number,
        tel = address.tel,
        city = address.city,
        cep = address.cep,
        state = address.state
    )
    order = Order.objects.create(user=user, price=price, address=infos_form)
    if metadata["type"] == "cart":
        cart = Cart.objects.get(id=metadata["cart_id"])
        items = cart.items.all()
        for item in items:
            OrderItem.objects.create(order=order, product=product, variant=variation, quantity=quantity)
            
    product = int(Product.objects.get(id=metadata["product_id"]))
    variation = Variation.objects.get(id=metadata["product_id"])
    quantity = metadata["quantity"]
    OrderItem.objects.create(order=order, product=product, variant=variation, quantity=quantity)
    return str(order.id)


def create_checkout_session_product(metadata, items, urls):
    order_id = create_order(metadata, items)
    metadata['order_id'] = order_id
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        mode="payment",
        success_url=f"http://localhost:8000/{urls['success_url']}",
        cancel_url=f"http://localhost:8000/{urls['cancel_url']}",
        metadata=metadata,
    )

    return session.url






