from django import views
from django.urls import path
from . import views



app_name = 'cart'

urlpatterns = [
    path("/", views.cart, name='cart'),
    path("add/<int:id>", views.add_to_cart, name='addcart'),
    path("buy/", views.cartbuy, name='cartbuy'),
    path("remove/", views.cartremove, name="cartremove"),
]