from django.db import transaction
from product.models import Product
from cart.models import CartItem
from .exceptions import OutOfStockError, MaxCartQuantity, CartItemNotExists
from payment.services import OrderCheckoutService
import random

class CartService:
    @transaction.atomic
    @staticmethod
    def AddCartProduct(user, product_id, variant_id, quantity):
        product = Product.objects.get(id=product_id)
        variant = product.variations.get(id=variant_id)
        quantity = int(quantity)
        if variant and variant.stock >= 1:
            item, created = CartItem.objects.get_or_create(
                cart=user.cart, product=product,
                variant=variant, defaults={'quantity': quantity})
            if not created:
                if item.quantity + quantity <= variant.stock:
                    item.quantity += quantity
                    item.save()
                    return
                raise MaxCartQuantity("A quantidade máxima já foi adicionada ao carrinho")
            return
        raise OutOfStockError("Produto sem estoque")

    @staticmethod
    def CartRemove(cart, id, variant_id):
        try:
            cart.items.get(id=id, variant=variant_id).delete()
        except CartItem.DoesNotExist:
            raise CartItemNotExists("O item não existe no carrinho")
    
    @staticmethod
    def items_random():
        items = list(Product.objects.filter(variations__stock__gt=0).distinct())
        random.shuffle(items)
        return items[:7]
    
    @staticmethod
    def return_itens(cart):
        items = cart.items.all()
        items_return = []
        for item in items:
            if item.variant.stock < item.quantity:
                item.quantity = item.variant.stock
                item.save()
                continue
            items_return.append(item)
        return items_return


    @staticmethod
    def CreateCartCheckout(user, address):
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
        url = OrderCheckoutService.create_checkout_session(metadata, line_items, urls)
        return url