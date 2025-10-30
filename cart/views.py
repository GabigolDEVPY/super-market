from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from product.models import Product
from cart.models import Cart, CartItem
from inventory.models import InventoryItem


@login_required(login_url='account:login')
def cart(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    items = cart.items.all()
    cart_price = cart.total_price
    
    return render(request ,"cart.html",
        context={"user": user,
        "cart_price": cart_price,
        "items": items })


@login_required(login_url='accounts:login')
def add_to_cart(request, id):
    user = request.user
    cart = user.cart
    product = Product.objects.get(id=id)
    if product.stocks.first().quantity:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
        if not created:
            item.quantity += 1
            item.save()
    

    return render(request ,"product.html",
        context={"product": product})

@login_required(login_url='accounts:login')
def cartbuy(request):
    user = request.user
    inventory = user.inventory
    cart = user.cart
    items = cart.items.all()
    for item in items:
        stock = item.product.stocks.first()
        inv_item, created = InventoryItem.objects.get_or_create(
            inventory=inventory, product=item.product)
        if not created:
            inv_item.quantity += item.quantity
            stock.quantity -= item.quantity
            stock.save()
            inv_item.save()
    items = cart.items.all().delete()
    return render(request, "cart.html")


@login_required(login_url='accounts:login')
def cartremove(request):
    if request.method == "POST":
        id = request.POST.get("id")
        user = request.user
        cart = user.cart
        cart.items.filter(id=id).delete()
        return redirect("cart:cart")
