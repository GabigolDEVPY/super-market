from django.urls import path
from . import webhooks


app_name = 'payment'

urlpatterns = [
    path("stripe/webhook/", webhooks.stripe_webhook, name='payment_webhook'),
    ]