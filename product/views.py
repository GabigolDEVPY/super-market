from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from product.models import Product
from django.views.generic.detail import DetailView
from inventory.models import InventoryItem, Inventory
from product.models import DiscountCode
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"
    context_object_name = "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object.stocks.first()
        context["quantity"] = stock.quantity if stock else 0 
        return context
    
class BuyNowView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        stock = product.stocks.first()
        if not stock or stock.quantity < 1:
            return render(request, "product.html", {"product": product})
        return render(request, "payment.html", {"product": product, "stock": stock})
    
    
    #apply discount cupom
    def post(self, request, id):
        discount = request.POST.get("discount") or None
        if discount:
            discount_search = DiscountCode.objects.filter(name=discount).first()
            if not discount_search:
                messages.error(request, "Cupom Inválido!")
                return redirect('product:buynow', id)
        product = Product.objects.get(id=id)
        stock = product.stocks.first()
        discount_price = product.price - (product.price / 100 * discount_search.discount)
        messages.success(request, "Cupom de desconto aplicado com sucesso!!")
        return render(request, 'payment.html', {"product": product, "stock": stock, "discount_price": discount_price})



@login_required(login_url='accounts:login')
def productbuynow(request):
    user = request.user
    quantity = int(request.POST.get("quantity"))
    id = request.POST.get("id")
    product = Product.objects.get(id=id)
    stock = product.stocks.first()
    if not stock or stock.quantity < quantity:
        return redirect("market:home")
    stock.quantity -= quantity
    stock.save()
    inventory, created = Inventory.objects.get_or_create(user=user)
    inventory_item = InventoryItem.objects.filter(inventory=inventory, product=product).first()
    
    if inventory_item:
        inventory_item.quantity += quantity
        inventory_item.save()
    else:
        InventoryItem.objects.create(inventory=inventory, product=product, quantity=quantity)
        
    return redirect("market:home")
    