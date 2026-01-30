from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import cartbuy, items_random, return_items
from .exceptions import OutOfStockError, MaxCartQuantity, CartItemNotExists
from .services import CartService


#retornar a tela do carrinho do cliente!
class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = items_random()
        context['address'] = self.request.user.address.all()
        context["items_cart"] = return_items(self.request)
        context["cart_price"] = self.request.user.cart.total_price
        return context
    

#Logica pra adicionar produto ao carrinho 
class AddCart(LoginRequiredMixin, View):
    def post(self, request):
        try:
            CartService.AddCartProduct(
                user=request.user, 
                product_id=request.POST.get("id"), 
                variant_id=request.POST.get("variantid"), 
                quantity=int(request.POST.get("quantity"))
                )
            messages.success(request, "Produto Adicionado ao carrinho", extra_tags="success")
            return redirect("product:product", request.POST.get("id"))
        except OutOfStockError as e:
            messages.error(request, str(e), extra_tags="danger")
            return redirect("product:product", request.POST.get("id"))
        except MaxCartQuantity as e:
            messages.warning(request, str(e), extra_tags="warning")
            return redirect("product:product", request.POST.get("id"))


# Logica pra remover item do carrinho 
class CartRemove(LoginRequiredMixin,View):
    def post(self, request):
        try:
            CartService.CartRemove(request.user.cart, request.POST.get("id"), request.POST.get("variant_id"))
        except CartItemNotExists as e:
            messages.error(request, str(e), extra_tags="danger")
        return redirect("cart:cart")


class CartBuyNow(View):
    def post(self, request, *args, **kwargs):
        url = CartService.CreateCartCheckout()
        return redirect(url)



