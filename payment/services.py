from django.contrib.auth.models import User
from accounts.models import Address
from product.models import Product, Variation
from payment.models import Order, OrderItem, InfosForm
from cart.models import Cart
import stripe
from django.conf import settings

stripe.api_key = settings.API_STRIPE

class OrderCheckoutService:
    @staticmethod
    def create_order(metadata, items):
        user = User.objects.get(id=metadata["user_id"])
        price = items[0]["price_data"]["unit_amount"] / 100
        address = Address.objects.get(id=metadata["address"])
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
            cart = Cart.objects.get(id=metadata["cart_id"])
            items = cart.items.all()
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, variant=item.variant, quantity=item.quantity)
            return str(order.id)
            
        product = Product.objects.get(id=metadata["product_id"])
        variation = Variation.objects.get(id=metadata["product_id"])
        quantity = metadata["quantity"]
        OrderItem.objects.create(order=order, product=product, variant=variation, quantity=quantity)
        return str(order.id)

    @staticmethod
    def create_checkout_session_product(metadata, items, urls):
        order_id = OrderCheckoutService.create_order(metadata, items)
        metadata['order_id'] = order_id
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items,
            mode="payment",
            success_url=f"http://localhost:8000/{urls['success_url']}",
            cancel_url=f"http://localhost:8000/{urls['cancel_url']}",
            metadata=metadata,
        )
        order = Order.objects.get(id=order_id)
        order.url = session.url
        order.save()
        return session.url






