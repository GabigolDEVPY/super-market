# product/webhooks.py

import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from product.models import Product
from django.contrib.auth.models import User
from inventory.models import Inventory, InventoryItem

@csrf_exempt
def stripe_webhook(request):
    print("chegou aqui")
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

        product_id = int(metadata["product_id"])
        user_id = int(metadata["user_id"])
        quantity = int(metadata["quantity"])

        # ATUALIZAÇÃO DO PEDIDO, ESTOQUE, INVENTÁRIO
        product = Product.objects.get(id=product_id)
        user = User.objects.get(id=user_id)

        # baixar estoque
        stock = product.stocks.first()
        stock.quantity -= quantity
        stock.save()

        # inventário
        inventory, _ = Inventory.objects.get_or_create(user=user)
        InventoryItem.objects.create(
            inventory=inventory,
            product=product,
            quantity=quantity,
        )

    return HttpResponse(status=200)
