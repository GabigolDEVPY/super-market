from django import views
from django.urls import path
from . import views



app_name = 'cart'

urlpatterns = [
    path("", views.CartView.as_view(), name='cart'),
    path("add/", views.AddCart.as_view(), name='addcart'),
    path("buy/", views.CartBuy.as_view(), name='cartbuy'),
    path("remove/", views.CartRemove.as_view(), name="cartremove"),
]