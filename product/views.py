from django.http import Http404
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
from payment.utils import create_checkout_session_product
from django.http import Http404


@method_decorator(clear_session_data(["discount_name", "discount_price"]), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variations_with_stock = self.object.variations.filter(stock__gt=0)
        stock = self.object.has_stock()
        context["quantity"] = self.object.variations.filter(stock__gt=0).first().stock if stock else None
        context["variants"] = variations_with_stock
        images = [img.image.url for img in  self.object.images.all()]
        images.insert(0, self.object.image.url)
        context["images"] = images

        return context
    
class BuyNowView(LoginRequiredMixin, View):
    def get(self, request, product_id, variant_id):
        product = Product.objects.get(id=product_id)
        variant = product.variations.get(id=variant_id)
        address = self.request.user.address.all()
        if not variant.stock or variant.stock < 1:
            raise Http404("product without stock avaliable")
        return render(request, "payment.html", {"product": product, "stock": variant.stock, "variant": variant, "address": address})
    
    
    #apply discount cupom
    def post(self, request, product_id, variant_id):
        discount = request.POST.get("discount") or None
        product = Product.objects.get(id=product_id)
        variant = product.variations.get(id=variant_id)
        address = self.request.user.address.all()
        stock = variant.stock
        previous_discount = request.session.get("discount_name")
        previous_price = request.session.get("discount_price", 0)
        
        if discount:
            discount_search = DiscountCode.objects.filter(name=discount).first()
            if not discount_search:
                messages.warning(request, "Cupom Inválido!", extra_tags="cupom")
                return render(request, 'payment.html', {"product": product, "stock": stock, "variant": variant, "address": address})
            discount_price = int(product.apply_discount() - (product.price / 100 * discount_search.discount))
            request.session["discount_name"] = discount_search.name
            request.session["discount_price"] = discount_price      
            messages.success(request, "Cupom de desconto aplicado com sucesso!!", extra_tags="cupom")
            # success cupom
            return render(request, 'payment.html', {"product": product, "stock": stock, "discount_price": discount_price, "variant": variant, "address": address})
        # error cupom
        messages.warning(request, "Insira um cupom de desconto!", extra_tags="cupom")
        return render(request, 'payment.html', {"product": product, "stock": stock, "variant": variant, "address": address})



@login_required(login_url='accounts:login')
def productbuynow(request):
    user = request.user
    quantity = int(request.POST.get("quantity"))
    id = request.POST.get("id")
    variant_id = request.POST.get("variant_id")
    product = Product.objects.get(id=id)
    if product.variations.get(id=variant_id).stock < quantity:
        raise Http404("product without stock avaliable")
    
    discount_price = request.session.get("discount_price")
    price = int(discount_price if discount_price else product.apply_discount) * 100
    #aprovar compra no checkout
    urls = {"success_url": "accounts/home/", "cancel_url": f"product/{id}"} 

    items = {
                "price_data": {
                    "currency": "brl",
                    "unit_amount": price,
                    "product": product.id_stripe,
                },
                "quantity": quantity
            },
        
    metadata={
            "product_id": str(id),
            "variant_id": str(variant_id),
            "user_id": str(user.id),
            "quantity": str(quantity),
            "event_mode": str("product"),
        }
    url = create_checkout_session_product(metadata, items, urls);
    return redirect(url)

    