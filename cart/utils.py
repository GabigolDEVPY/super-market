from urllib import response
from django.shortcuts import redirect
from product.models import Product
from cart.models import CartItem
from django.http import HttpResponse
import requests
from product.models import Variation
from payment.utils import create_checkout_session_product
import random

def add_to_cart(request):
    user = request.user
    cart = user.cart
    variant_id = request.POST.get("variantid")
    id = request.POST.get("id")
    quantity = int(request.POST.get("quantity"))
    product = Product.objects.get(id=id)
    variant = product.variations.get(id=variant_id)
    if variant and variant.stock >= 1:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, variant=variant, defaults={'quantity': quantity,})
        if not created:
            item.quantity += quantity
            item.save()
    return id
    

def cartremove(request):
    print("entrou aqui krl")
    try:
        print("entrou no try")
        id = request.POST.get("id")
        variant_id = request.POST.get("variant_id")
        user = request.user
        cart = user.cart
        item_cart = cart.items.filter(id=id, variant=variant_id).delete()
        cart.save()
    except Exception as e:
        return HttpResponse(status=200)
    
    
def cartbuy(request):
    user = request.user
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
    }
    return redirect(create_checkout_session_product(metadata, line_items, urls))


def items_random():
    items = list(Product.objects.filter(variations__stock__gt=0).distinct())
    random.shuffle(items)
    return items[:7]

def return_items(user):
    items = user.cart.items.all()
    items_return = []
    for item in items:
        if item.variant.stock < item.quantity:
            item.delete()
            continue
        items_return.append(item)
    return items_return
    