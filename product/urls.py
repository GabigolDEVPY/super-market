from django import views
from django.urls import path
from . import views, webhooks


app_name = 'product'

urlpatterns = [
    # product.views
    path("<int:pk>/", views.ProductDetailView.as_view(), name='product'),
    path("buy/<int:id>/", views.BuyNowView.as_view(), name='buynow'),
    path("buy/", views.productbuynow, name='productbuynow'),
    path("stripe/webhook/", webhooks.stripe_webhook)
]