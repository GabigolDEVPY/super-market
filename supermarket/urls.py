from django import views
from django.contrib import admin
from django.urls import path
from supermarket import views


app_name = "market"

urlpatterns = [
    path("products/all", views.home)
]