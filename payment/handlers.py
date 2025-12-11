from django.contrib.auth.models import User
from accounts.models import InventoryItem, Inventory
import product
from product.models import Product

class TempItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

def payment(metadata):
    user = User.objects.get(id=metadata["user_id"])
    inventory = user.inventory
    if metadata["event_mode"] == "cart":
        cart = user.cart
        items = cart.items.all() 
    elif metadata["event_mode"] == "product":
        product = Product.objects.get(id=metadata["product_id"])
        quantity = int(metadata["quantity"])
        items = [TempItem(product, quantity)]
        
    for item in items:
        stock = item.product.stocks.first()
        inv_item, created = InventoryItem.objects.get_or_create(
            inventory=inventory, product=item.product)
        if not created:
            inv_item.quantity += item.quantity
            stock.quantity -= item.quantity
            stock.save()
            inv_item.save()
        if metadata["event_mode"] == "cart":
            cart.items.all().delete()
    
    