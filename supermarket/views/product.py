from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from supermarket.models import Cart, InventoryItem, Product, CartItem, Inventory


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
    user = request.user
    quantity = request.POST.get("quantity") if request.POST.get("quantity") else 1
    id = request.POST.get("id")
    discount = request.POST.get("discount") or None
    inventory, created = Inventory.objects.get_or_create(user=user)
    product = Product.objects.get(id=id)
    InventoryItem.objects.create(inventory=inventory, product=product, quantity=quantity)
    
    return redirect("market:home")
    