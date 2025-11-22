# product/webhooks.py

import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from cart.models import Cart
import product
from product.models import Product
from django.contrib.auth.models import User
from inventory.models import Inventory, InventoryItem

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except Exception:
        return HttpResponse(status=400)
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session["metadata"]
        user = metadata["user_id"]
        if metadata["event_mode"] == "cart":
            cart = Cart.objects.get(id=metadata["cart_id"])
            inventory = Inventory.objects.get(user=metadata["user_id"])
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
            return HttpResponse(status=200)
        elif metadata["event_mode"] == "product":
            print("have a product here")    
            quantity = int(metadata["quantity"])
            product = Product.objects.get(id=metadata["product_id"])   
            stock = product.stocks.first()
            stock.quantity -= quantity
            stock.save()
            inventory, created = Inventory.objects.get_or_create(user=metadata["user_id"])
            inventory_item, _= InventoryItem.objects.get_or_create(inventory=inventory, product=product)  
            inventory_item.quantity += quantity
            inventory_item.save()
            return HttpResponse(status=200)
        return HttpResponse(status=200)
