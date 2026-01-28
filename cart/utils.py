from django.shortcuts import redirect
from product.models import Product
from cart.models import CartItem
from django.http import HttpResponse
from payment.utils import create_checkout_session_product
import random


def cartremove(request):
    try:
        cart = request.user.cart
        item_cart = cart.items.get(id=request.POST.get("id"), variant=request.POST.get("variant_id")).delete()
        cart.save()
    except Exception as e:
        return HttpResponse(status=200)
    
    
def cartbuy(request):
    user = request.user
    address = int(request.POST.get("address"))
    urls = {"success_url": "accounts/home/", "cancel_url": "cart/"} 
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
        "event_mode": "cart",
        "type": "cart",
        "cart_id": str(user.cart.id),
        "user_id": str(user.id),
        "address": address
    }
    url = create_checkout_session_product(metadata, line_items, urls)
    return url


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
