import stripe
from django.shortcuts import render, redirect
from django.http import Http404

import os


stripe.api_key = os.getenv("API_KEY_STRIPE")

def create_checkout_session(unit_amount, quantity):
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            success_url="https://seusite.com/success",
            cancel_url="http://127.0.0.1:8000/",
            line_items=[{"price_data": {"currency": "brl", "unit_amount": unit_amount, "product": "prod_TQkRWppUtfASmD"}, "quantity": quantity }],
        )
    except Exception as e:
        raise Http404("Erro ao carregar checkout")
        
    return session.url

