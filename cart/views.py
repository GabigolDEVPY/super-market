from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from product.models import Product
from cart.models import Cart, CartItem
from inventory.models import InventoryItem
from utils.decorators import clear_session_data
from django.utils.decorators import method_decorator


@method_decorator(clear_session_data(["discount_price", "discount_name"]), name="dispatch")
class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.request.user.cart.items.all()
        context["cart_price"] = self.request.user.cart.total_price
        return context 
    

@login_required(login_url='accounts:login')
def add_to_cart(request, id):
    user = request.user
    cart = user.cart
    product = Product.objects.get(id=id)
    
    
    if product.discount:
        discount_amount = (product.price * product.discount.discount) / 100
        final_price = product.price - discount_amount
    else:
        final_price = product.price
    stock = product.stocks.first()
    if  not stock or stock.quantity < 1:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1,})
        
        if not created:
            item.quantity += 1
            item.save()
    

    return redirect("product:product", product.id)

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
