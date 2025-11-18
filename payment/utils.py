# product/utils.py

import stripe
from django.conf import settings

stripe.api_key = settings.API_STRIPE

def create_checkout_session(price, quantity, product, user):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "brl",
                "unit_amount": price,
                "product_data": {
                    "name": product.name,
                },
            },
            "quantity": quantity,
        }],
        mode="payment",
        success_url="http://localhost:8000/inventory",
        cancel_url="http://localhost:8000/",
        metadata={
            "product_id": str(product.id),
            "user_id": str(user.id),
            "quantity": str(quantity),
        }
    )

    return session.url

