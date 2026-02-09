from product.models import Product, Variation
from product.models import DiscountCode
from payment.services import OrderCheckoutService


class ProductService:   
    @staticmethod
    def aplly_discount(discount, product_id, variant_id, user):
        discount = discount
        product = Product.objects.get(id=product_id)
        variant = Variation.objects.get(id=variant_id, product=product_id)
        address = user.address.all()
        stock = variant.stock
        if discount:
            discount_search = DiscountCode.objects.filter(name=discount).first()
            if not discount_search:
                return {"error": "Cupom de desconto inválido"}, False
            discount_price = int(variant.apply_discount() - (variant.price / 100 * discount_search.discount))
            return (
                {"discount_price": discount_price,"discount_name": discount_search.name, "message": "Cupom de desconto aplicado com sucesso!"},
                {"product": product, "stock": stock, "variant": variant, "address": address}
            )
        return {"error": "Insira um cupom de desconto"}, False
    
    @staticmethod
    def get_product_data(product):
        variations_with_stock =product.variations.filter(stock__gt=0)
        stock=product.has_stock()   
        quantity = variations_with_stock.first().stock if product.has_stock else None
        images = [img.image.url for img in product.images.all()]
        images.insert(0, product.image.url)
        
        return {
            "variants": variations_with_stock,
            "quantity": quantity,
            "images": images
        }
    
    @staticmethod
    def get_payment_data(product_id, variant_id, user):
        product = Product.objects.get(id=product_id)
        variant = product.variations.get(id=variant_id)
        address = user.address.all()
        return {"product": product, "stock": variant.stock, "variant": variant, "address": address}
    
    @staticmethod
    def product_buy_now(quantity, product_id, variant_id, address_id, discount_price, user_id):
        product = Product.objects.get(id=product_id)
        variant = product.variations.get(id=variant_id)
        price = int(float(variant.apply_discount()) * 100)
        if discount_price:
            price = int(float(discount_price) * 100)
        
        context = {
            "urls": {
                "success_url": "accounts/home/",
                "cancel_url": f"product/{product_id}",
            },
            "items": [{
                "price_data": {
                    "currency": "brl",
                    "unit_amount": price,
                    "product": product.id_stripe,
                },
                "quantity": int(quantity)
            }],
            "metadata": {
                "type": "product",
                "product_id": int(product_id),
                "variant_id": str(variant_id),
                "address": str(address_id),
                "user_id": str(user_id),
                "quantity": int(quantity),
                "event_mode": "product",
                "total_price": price,
            }
        }
        url = OrderCheckoutService.create_checkout_session(**context);
        return url
