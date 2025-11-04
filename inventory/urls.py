from django import views
from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path("", views.InventoryView.as_view(), name="inventory")
]