from decimal import Decimal
from accounts.models import Address
import product
from product.models import Product, Variation
from payment.models import Order, OrderItem, InfosForm
from django.contrib.auth import get_user_model
from cart.models import Cart
import stripe
from django.db import transaction
from django.conf import settings
from . exceptions import (EmptyCartException, InvalidCheckoutMetadata)

stripe.api_key = settings.API_STRIPE

class OrderCheckoutService:
    @transaction.atomic    
    @staticmethod
    def create_order(metadata, items):
        User = get_user_model()
        user = User.objects.get(id=metadata["user_id"])
        price = Decimal(metadata["total_price"])
        address = Address.objects.get(id=metadata["address"], user=user)
        infos_form = InfosForm.objects.create(
            user = user,
            address = address.address,
            complement = address.complement,
            neighborhood = address.neighborhood,
            number = address.number,
            tel = address.tel,
            city = address.city,
            cep = address.cep,
            state = address.state
        )
        order = Order.objects.create(user=user, price=price, address=infos_form)
        if metadata["type"] == "cart":
            cart = Cart.objects.get(id=metadata["cart_id"], user=user)
            items = cart.items.select_related("product", "variant")
            if not cart.items.exists():
                raise EmptyCartException("Sem itens no carrinho")
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, variant=item.variant, quantity=item.quantity)
            return str(order.id)
        product = Product.objects.get(id=metadata["product_id"])
        variation = Variation.objects.get(id=metadata["variant_id"])
        quantity = metadata["quantity"]
        OrderItem.objects.create(order=order, product=product, variant=variation, quantity=quantity)
        return str(order.id)

    @transaction.atomic
    @staticmethod
    def create_checkout_session(metadata, items, urls):
        order_id = OrderCheckoutService.create_order(metadata, items)
        metadata['order_id'] = order_id
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            success_url=f"{settings.FRONTEND_URL}/{urls['success_url']}",
            cancel_url=f"{settings.FRONTEND_URL}/{urls['cancel_url']}",
            metadata=metadata,
        )
        order = Order.objects.get(id=order_id)
        order.url = session.url
        order.save()
        return session.url

    @transaction.atomic
    @staticmethod
    def post_paid(metadata):
        User = get_user_model()
        user = User.objects.get(id=metadata["user_id"])
        cart = user.cart
        order = Order.objects.get(id=metadata["order_id"], user=user)
        if not user:
            raise InvalidCheckoutMetadata("Id de usuário inválido")
        if order.status == "A":
            return        
        order.status = "A"
        order.save()
        if metadata["event_mode"] == "cart":
            for item in cart.items.select_related("product", "variant"):
                item.variant.stock -= item.quantity
                item.variant.save()
            cart.items.all().delete()
            cart.save()
        else:
            variant = Variation.objects.get(
                id=metadata["variant_id"], 
                product=metadata["product_id"])
            variant.stock -= int(metadata["quantity"])
            variant.save()
        



