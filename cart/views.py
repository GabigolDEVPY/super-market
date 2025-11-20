from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import  TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator
from inventory.models import InventoryItem
from .utils import add_to_cart


#retornar a tela do carrinho do cliente!
@method_decorator(clear_session_data(["discount_price", "discount_name"]), name="dispatch")
class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.request.user.cart.items.all()
        context["cart_price"] = self.request.user.cart.total_price
        return context 
    

#Logica pra adicionar produto ao carrinho 
class AddCart(LoginRequiredMixin, View):
    def get(self, request, id):
        product = add_to_cart(request, id)
        return redirect("product:product", product.id)


#Rota pra comprar itens do carrinho 
@login_required(login_url='accounts:login')
def cartbuy(request):
    user = request.user
    inventory = user.inventory
    cart = user.cart
    items = cart.items.all()
    for item in items:
        stock = item.product.stocks.first()
        inv_item, created = InventoryItem.objects.get_or_create(
            inventory=inventory, product=item.product)
        if not created:
            inv_item.quantity += item.quantity
            stock.quantity -= item.quantity
            stock.save()
            inv_item.save()
    items = cart.items.all().delete()
    return render(request, "cart.html")


@login_required(login_url='accounts:login')
def cartremove(request):
    if request.method == "POST":
        id = request.POST.get("id")
        user = request.user
        cart = user.cart
        cart.items.filter(id=id).delete()
        return redirect("cart:cart")
