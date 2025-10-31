from django import views
from django.urls import path
from . import views



app_name = 'cart'

urlpatterns = [
    path("cart/", views.cart, name='cart'),
    path("cart/add/<int:id>", views.add_to_cart, name='addcart'),
    path("cart/buy", views.cartbuy, name='cartbuy'),
    path("cart/remove", views.cartremove, name="cartremove"),
]