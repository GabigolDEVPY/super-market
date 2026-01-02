# product/utils.py
from django.shortcuts import redirect
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from accounts.models import InventoryItem
import requests
import stripe
from django.conf import settings

stripe.api_key = settings.API_STRIPE

def create_checkout_session_product(metadata, items, urls):
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
    print("entrou aqui")
    form = request.POST.dict()
    user = request.user
    return redirect(create_checkout_session_product(metadata, line_items, urls))



