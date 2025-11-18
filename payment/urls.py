from django.shortcuts import render
from django.urls import path
from . import views, webhooks

app_name = 'payment'

urlpatterns = [
    path("stripe/webhook/", webhooks.stripe_webhook, name='payment')
    ]