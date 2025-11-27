from django.shortcuts import render
from django.urls import path

from payment.utils import paymentbuy
from . import views, webhooks

app_name = 'payment'

urlpatterns = [
    path("payment/stripe/webhook/", webhooks.stripe_webhook, name='payment_webhook'),
    path("payment/validade", views.PaymentValidate.as_view() , name="validate"),
    path("payment/buy", views.PaymentBuy.as_view() , name="payment")
    ]