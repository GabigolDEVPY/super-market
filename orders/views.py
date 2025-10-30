from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from supermarket.models import Cart, InventoryItem, Products, CartItem, Inventory

# Create your views here.
@login_required(login_url='market:login')
def inventory(request):
    user = request.user
    inventory = user.inventory
    items = inventory.items.all()
    return render(request, "inventory.html", context={"items": items})