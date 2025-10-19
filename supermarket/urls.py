from django import views
from django.contrib import admin
from django.urls import path
from supermarket import views


app_name = 'market'

urlpatterns = [
    #home
    path("", views.home, name="home"),
    
    path("products/all/", views.home, name='product'),
    path("user/create/", views.register_user, name='register'),
]