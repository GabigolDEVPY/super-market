from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from supermarket.models import Cart, Product, CartItem


@login_required(login_url='market:login')
def home(request):
    user = request.user
    products = Product.objects.all()
    return render(request ,"home.html",
        context={
            "products": products
        })

@login_required(login_url='market:login')
def product(request, id):
    product = Product.objects.get(id=id)
    return render(request ,"product.html",
        context={"product": product})

