from django import dispatch
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


@method_decorator(clear_session_data(["discount_name", "discount_price"]), name="dispatch")
class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object.has_stock()
        context["quantity"] = self.object.variations.first().stock if stock else None
        images = [img.image.url for img in  self.object.images.all()]
        images.insert(0, self.object.image.url)
        context["images"] = images

        return context
    
class BuyNowView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        stock = product.stocks.first()
        if not stock or stock.quantity < 1:
            return render(request, "payment.html", {"product": product})
        return render(request, "payment.html", {"product": product, "stock": stock})
    
    
    #apply discount cupom
    def post(self, request, id):
        discount = request.POST.get("discount") or None
        product = Product.objects.get(id=id)
        stock = product.stocks.first()
        previous_discount = request.session.get("discount_name")
        previous_price = request.session.get("discount_price", 0)
        
        if discount:
            discount_search = DiscountCode.objects.filter(name=discount).first()
            if not discount_search:
                previous_discount = request.session.get("discount_name")
                previous_price = request.session.get("discount_price")
                messages.error(request, "Cupom Inválido!")
                return render(request, 'payment.html', {"product": product, "stock": stock, "discount_price": previous_price, "discount": previous_discount})
            discount_price = float(product.apply_discount() - (product.price / 100 * discount_search.discount))
            request.session["discount_name"] = discount_search.name
            request.session["discount_price"] = discount_price      
            messages.success(request, "Cupom de desconto aplicado com sucesso!!")
            return render(request, 'payment.html', {"product": product, "stock": stock, "discount_price": discount_price})
        messages.success(request, "Insira um cupom de desconto!!")
        return render(request, 'payment.html', {"product": product, "stock": stock, "discount_price": previous_price})



@login_required(login_url='accounts:login')
def productbuynow(request):
    user = request.user
    quantity = int(request.POST.get("quantity"))
    id = request.POST.get("id")
    product = Product.objects.get(id=id)
    stock = product.stocks.first()
    if not stock or stock.quantity < quantity:
        return redirect("market:home")
    
    discount_price = request.session.get("discount_price")
    if discount_price is not None:
        price = int(discount_price * 100)
    else:
        price = int(product.price * 100)
        
    #aprovar compra no checkout
    urls = {"success_url": "inventory/", "cancel_url": f"product/{id}"} 
 
    items = {
                "price_data": {
                    "currency": "brl",
                    "unit_amount": int((product.apply_discount()) * 100),
                    "product": product.id_stripe,
                },
                "quantity": quantity
            },
        
    metadata={
            "product_id": str(product.id),
            "user_id": str(user.id),
            "quantity": str(quantity),
        }
    url = create_checkout_session_product(metadata, items, urls);
    return redirect(url)

    