from django import views
from django.contrib import admin
from django.urls import path
from supermarket import views


app_name = 'market'

urlpatterns = [
    #home
    path("", views.home, name='home'),
    path("cart/", views.cart, name='cart'),
    
    path("login/", views.login_user, name='login'),
    path("register/", views.register_user, name='register'),
    path("logout/", views.logout_user, name="logout")
]