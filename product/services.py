from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from product.models import Product, Variation
from django.views.generic.detail import DetailView
from product.models import DiscountCode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from payment.services import OrderCheckoutService
from django.http import Http404



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
    
    def get_payment_data(product_id, variant_id, user):
        product = Product.objects.get(id=product_id)
        variant = product.variations.get(id=variant_id)
        address = user.address.all()
        return {"product": product, "stock": variant.stock, "variant": variant, "address": address}