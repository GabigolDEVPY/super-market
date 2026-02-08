from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from product.models import Product
from django.views.generic.detail import DetailView
from product.models import DiscountCode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from payment.services import OrderCheckoutService
from django.http import Http404
from . services import ProductService


@method_decorator(clear_session_data(["discount_name", "discount_price"]), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_data = ProductService.get_product_data(self.object)
        context.update(product_data)
        return context
    
class BuyNowView(LoginRequiredMixin, View):
    # route buy product
    def get(self, request, product_id, variant_id):
        context_data = ProductService.get_payment_data(product_id, variant_id, request.user)
        return render(request, "payment.html", context=context_data)
    
    #apply discount cupom
    def post(self, request, product_id, variant_id):
        response, context = ProductService.aplly_discount(request.POST.get("discount"), product_id, variant_id, self.request.user)
        if "error" in response:
            messages.warning(request, response["error"], extra_tags="warning")
            return redirect("product:buynow", product_id=product_id, variant_id=variant_id)
        request.session["discount_price"] = response["discount_price"]    
        request.session["discount_name"] = response["discount_name"]   
        messages.success(request, response["message"], extra_tags="success")
        return render(request, 'payment.html', context=context)




@login_required(login_url='accounts:login')
def productbuynow(request):
    user = request.user
    quantity = int(request.POST.get("quantity"))
    product_id = request.POST.get("id")
    variant_id = request.POST.get("variant_id")
    address_id = request.POST.get("address")
    product = Product.objects.get(id=product_id)
    variant = product.variations.get(id=variant_id)
    if variant.stock < quantity:
        raise Http404("product without stock avaliable")
    
    discount_price = request.session.get("discount_price")
    price = int(float(variant.apply_discount()) * 100)
    if discount_price:
        price = int(float(discount_price) * 100)
        
    urls = {"success_url": "accounts/home/", "cancel_url": f"product/{product_id}"} 

    items = {
                "price_data": {
                    "currency": "brl",
                    "unit_amount": price,
                    "product": product.id_stripe,
                },
                "quantity": quantity
            },
        
    metadata={
            "type": "product",
            "product_id": int(product_id),
            "variant_id": str(variant_id),
            "address": str(address_id),
            "user_id": str(user.id),
            "quantity": int(quantity),
            "event_mode": str("product"),
            "total_price": price
        }
    url = OrderCheckoutService.create_checkout_session(metadata, items, urls);
    return redirect(url)

    