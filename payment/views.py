from django.shortcuts import render
from django.urls import path
from . import views, webhooks

urlpatterns = path("stripe/webhook/", webhooks.stripe_webhook)