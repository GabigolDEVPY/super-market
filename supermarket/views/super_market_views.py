from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from supermarket.models import Cart, Product

# Create your views here.

@login_required(login_url='market:login')
def home(request):
    user = request.user
    products = Product.objects.all()
    return render(request ,"home.html",
        context={
            "products": products
        })

@login_required(login_url='market:login')
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    items = cart.items.all()
    cart_price = cart.total_price
    
    
    return render(request ,"cart.html",
        context={"user": user,
        "cart_price": cart_price,
        "items": items })