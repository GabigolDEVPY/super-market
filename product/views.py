from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from product.models import Product
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
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
    url = ProductService.product_buy_now(
        quantity=request.POST.get("quantity"), product_id=request.POST.get("id"),
        variant_id=request.POST.get("variant_id"), address_id=request.POST.get("address"),
        discount_price=request.session.get("discount_price"), user_id=request.user.id
    )
    return redirect(url)

    