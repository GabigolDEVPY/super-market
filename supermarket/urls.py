from django import views
from django.contrib import admin
from django.urls import path
from supermarket import views


app_name = 'market'

urlpatterns = [
    path("", views.home, name='home'),
    path("cart/", views.cart, name='cart'),
    path("cart/add/<int:id>", views.add_to_cart, name='addcart'),
    path("product/<int:id>/", views.product, name='product'),
    
    path("login/", views.login_user, name='login'),
    path("register/", views.register_user, name='register'),
    path("logout/", views.logout_user, name="logout")
]