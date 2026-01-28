from django.db import transaction
from product.models import Product
from cart.models import CartItem
from django.core.exceptions import ValidationError
from .cart_exceptions import OutOfStockError, MaxCartQuantity

class CartService():
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
    def CartRemove