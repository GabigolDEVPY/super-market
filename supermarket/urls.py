from django import views
from django.contrib import admin
from django.urls import path
from supermarket import views
from supermarket.admin import Inventory


app_name = 'market'

urlpatterns = [
    # home
    path("", views.home, name='home'),
    
    # my purchases
    path("mypurchases/", views.inventory, name="inventory"),

    # cart views
    path("cart/", views.cart, name='cart'),
    path("cart/add/<int:id>", views.add_to_cart, name='addcart'),
    path("cart/buy", views.cartbuy, name='cartbuy'),
    path("cart/remove", views.cartremove, name="cartremove"),

    # product.views
    path("product/<int:id>/", views.product, name='product'),
    path("product/buy/<int:id>/", views.buynow, name='buynow'),
    path("product/buy", views.productbuynow, name='productbuynow'),

    
    # user views
    path("login/", views.login_user, name='login'),
    path("register/", views.register_user, name='register'),
    path("logout/", views.logout_user, name="logout")
]