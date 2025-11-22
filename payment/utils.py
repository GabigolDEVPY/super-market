# product/utils.py

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

