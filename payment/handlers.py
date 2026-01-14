from django.contrib.auth.models import User
from accounts.models import InventoryItem
from product.models import Product
from .models import Order

class TempItem:
    def __init__(self, product, variant, quantity):
        self.product = product
        self.variant = variant
        self.quantity = quantity

def payment(metadata):
    print("chamou payment")
    user = User.objects.get(id=metadata["user_id"])
    cart = user.cart
    inventory = user.inventory
    order = Order.objects.get(id=metadata["order_id"])
    order.status = "A"
    order.save()
    if metadata["event_mode"] == "cart":
        items = user.cart.items.all() 
    elif metadata["event_mode"] == "product":
        product = Product.objects.get(id=metadata["product_id"])
        items = [TempItem(
            product=product,
            variant=product.variations.get(id=metadata["variant_id"]),
            quantity=int(metadata["quantity"])
            )]
        
    for item in items:
        inv_item, created = InventoryItem.objects.get_or_create(
            inventory=inventory, product=item.product, variant=item.variant)
        item.variant.stock -= item.quantity
        item.variant.save()
        if not created:
            inv_item.quantity += item.quantity
            inv_item.save()
    if metadata["event_mode"] == "cart":
        cart.items.all().delete()
        cart.save()
    
    