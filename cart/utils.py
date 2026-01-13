from django.shortcuts import redirect
from product.models import Product
from cart.models import CartItem
from django.http import HttpResponse
from payment.utils import create_checkout_session_product
import random

def add_to_cart(request):
    product = Product.objects.get(id=request.POST.get("id"))
    variant = product.variations.get(id=request.POST.get("variantid"))
    quantity = int(request.POST.get("quantity"))
    if variant and variant.stock >= 1:
        item, created = CartItem.objects.get_or_create(
            cart= request.user.cart, 
            product= product,
            variant= variant, 
            defaults={'quantity': quantity})
        if not created:
            if variant.stock > item.quantity:
                item.quantity += quantity
                item.save()
            return product.id, True
    return product.id, False
    

def cartremove(request):
    try:
        cart = request.user.cart
        item_cart = cart.items.get(id=request.POST.get("id"), variant=request.POST.get("variant_id")).delete()
        cart.save()
    except Exception as e:
        return HttpResponse(status=200)
    
    
def cartbuy(request):
    user = request.user
    address = request.POST.get("address")
    urls = {"success_url": "inventory/", "cancel_url": "cart/"} 
    line_items = [
            {
                "price_data": {
                    "currency": "brl",
                    "unit_amount": int((item.product.apply_discount()) * 100),
                    "product": item.product.id_stripe,
                },
                "quantity": item.quantity
            }
        for item in user.cart.items.all()]
    
    metadata={
        "cart_id": str(user.cart.id),
        "user_id": str(user.id),
        "address": address
    }
    return redirect(create_checkout_session_product(metadata, line_items, urls))


def items_random():
    items = list(Product.objects.filter(variations__stock__gt=0).distinct())
    random.shuffle(items)
    return items[:7]

def return_items(request):
    items = request.user.cart.items.all()
    items_return = []
    for item in items:
        if item.variant.stock < item.quantity:
            item.quantity = item.variant.stock
            continue
        items_return.append(item)
    return items_return
