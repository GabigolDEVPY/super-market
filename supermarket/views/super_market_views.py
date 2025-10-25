from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    stock = product.stocks.first()
    quantity = stock.quantity if stock else 0
    return render(request ,"product.html",
        context={
            "product": product,
            "quantity": quantity
            })

@login_required(login_url='market:login')
def buynow(request, id):
    product = Product.objects.get(id=id)
    return render(request ,"payment.html",
        context={"product": product})

@login_required(login_url='market:login')
def productbuynow(request):
    pass