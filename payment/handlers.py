from django.contrib.auth.models import User
from product.models import Product
from .models import Order

class TempItem:
    def __init__(self, product, variant, quantity):
        self.product = product
        self.variant = variant
        self.quantity = quantity


def payment(metadata):
    user = User.objects.get(id=metadata["user_id"])
    cart = user.cart
    Order.objects.get(id=metadata["order_id"]).status = "A"
    if metadata["event_mode"] == "cart":
        items = cart.items.all() 
    elif metadata["event_mode"] == "product":
        product = Product.objects.get(id=metadata["product_id"])
        items = [TempItem(
            product=product,
            variant=product.variations.get(id=metadata["variant_id"]),
            quantity=int(metadata["quantity"])
            )]        
    if metadata["event_mode"] == "cart":
        cart.items.all().delete()
        cart.save()
    
    