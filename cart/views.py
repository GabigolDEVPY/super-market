from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from .utils import add_to_cart, cartremove, cartbuy, items_random, return_items
from payment.utils import create_checkout_session_product


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
        id, error = add_to_cart(request)
        if error:
            messages.error(request, "A quantidade máxima já foi adicionada ao carrinho")
            return redirect("product:product", id)
        return redirect("product:product", id)


# Logica pra remover item do carrinho 
class CartRemove(LoginRequiredMixin,View):
    def post(self, request):
        print("teste")
        cartremove(request)
        return redirect("cart:cart")



class CartBuyNow(View):
    def post(self, request, *args, **kwargs):
        dados = cartbuy(request)
        redirect("payment:cart")



