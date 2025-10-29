from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from supermarket.models import Cart, InventoryItem, Products, CartItem, Inventory


def product(request, id):
    product = Products.objects.get(id=id)
    stock = product.stocks.first()
    quantity = stock.quantity if stock else 0
    return render(request ,"product.html",
        context={
            "product": product,
            "quantity": quantity
            })

@login_required(login_url='market:login')
def buynow(request, id):
    product = Products.objects.get(id=id)
    stock = product.stocks.first()
    return render(request ,"payment.html",
        context={
                "product": product,
                "stock": stock
                })

@login_required(login_url='market:login')
def productbuynow(request):
    user = request.user
    quantity = int(request.POST.get("quantity"))
    id = request.POST.get("id")
    discount = request.POST.get("discount") or None
    product = Products.objects.get(id=id)
    stock = product.stocks.first()
    if not stock or stock.quantity < quantity:
        return redirect("market:home")
    stock.quantity -= quantity
    stock.save()
    inventory, created = Inventory.objects.get_or_create(user=user)
    inventory_item = InventoryItem.objects.filter(inventory=inventory, product=product).first()
    
    if inventory_item:
        inventory_item.quantity += quantity
        inventory_item.save()
    else:
        InventoryItem.objects.create(inventory=inventory, product=product, quantity=quantity)
        
    return redirect("market:home")
    