# product/utils.py

import stripe
from django.conf import settings

stripe.api_key = settings.API_STRIPE

def create_checkout_session_product(metadata, items):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        mode="payment",
        success_url="http://localhost:8000/inventory",
        cancel_url=f"http://localhost:8000/product/",
        metadata=metadata
    )

    return session.url

