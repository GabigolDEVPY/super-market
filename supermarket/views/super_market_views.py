from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from supermarket.models import Cart, InventoryItem, Product, CartItem, Inventory


def home(request):
    user = request.user
    products = Product.objects.all()
    return render(request ,"home.html",
        context={
            "products": products
        })

@login_required(login_url='market:login')
def inventory(request):
    user = request.user
    inventory = user.inventory
    items = inventory.items.all()
    return render(request, "inventory.html", context={"items": items})
    