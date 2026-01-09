# product/utils.py
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from accounts.models import InventoryItem
from payment.models import Order, OrderItem
import requests
import stripe
from django.conf import settings

stripe.api_key = settings.API_STRIPE

def create_order(metadata, items):
    user = User.objects.get(id=metadata["user_id"])
    print(items[0]["price_data"]["unit_amount"])
    # Order.objects.create(user=user, price=items[0]["unit_amount"])


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



