from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from supermarket.models import Cart, InventoryItem, Products, CartItem, Inventory


def home(request):
    user = request.user
    products = Products.objects.all()
    return render(request ,"home.html",
        context={
            "products": products
        })

    