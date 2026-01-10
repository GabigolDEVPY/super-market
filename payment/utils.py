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
from payment.models import Order, OrderItem, InfosForm
import requests
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
    Order.objects.create(user=user, price=price, address=infos_form)


def create_checkout_session_product(metadata, items, urls):
    create_order(metadata, items)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        mode="payment",
        success_url=f"http://localhost:8000/{urls["success_url"]}",
        cancel_url=f"http://localhost:8000/{urls["cancel_url"]}",
        metadata=metadata
    )

    return session.url


def paymentbuy(request):
    form = request.POST.dict()
    user = request.user
    return redirect(create_checkout_session_product(metadata, line_items, urls))



