from django.shortcuts import redirect
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from .utils import add_to_cart, cartremove, cartbuy, items_random



#retornar a tela do carrinho do cliente!
@method_decorator(clear_session_data(["discount_price", "discount_name"]), name="dispatch")
class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = items_random()
        context['address'] = self.request.user.address.all()
        context["items_cart"] = self.request.user.cart.items.all()
        context["cart_price"] = self.request.user.cart.total_price
        return context
    


#Logica pra adicionar produto ao carrinho 
class AddCart(LoginRequiredMixin, View):
    def post(self, request):
        id = add_to_cart(request)
        return redirect("product:product", id)


# Logica pra remover item do carrinho 
class CartRemove(LoginRequiredMixin,View):
    def post(self, request):
        cartremove(request)
        return redirect("cart:cart")

#Rota pra comprar itens do carrinho 
class CartBuy(LoginRequiredMixin, View):
    def get(self, request):
        dados = cartbuy(request)
        redirect("payment:cart")
    



