from django import views
from django.urls import path
from product import views


app_name = 'product'

urlpatterns = [
    path("<int:pk>/", views.ProductDetailView.as_view(), name='product'),
    path("buy/<int:product_id>/variant/<int:variant_id>/",views.BuyNowView.as_view(),name="buynow"),
    path("buy/", views.productbuynow, name='productbuynow'),
]