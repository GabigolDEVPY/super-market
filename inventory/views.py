from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from product.models import Product
from cart.models import Cart, CartItem
from django.contrib.auth.models import User
from inventory.models import InventoryItem, Inventory

# Create your views here.
@login_required(login_url='accounts:login')
def inventory(request):
    user = request.user
    inventory = user.inventory
    items = inventory.items.all()
    return render(request, "inventory.html", context={"items": items})