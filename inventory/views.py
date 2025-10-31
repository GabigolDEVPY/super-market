from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from product.models import Product
from cart.models import Cart, CartItem
from inventory.models import InventoryItem

# Create your views here.
def inventory(request):
    pass