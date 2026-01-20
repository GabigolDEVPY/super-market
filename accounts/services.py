from django.shortcuts import get_object_or_404
from .utils import validade_cep
from .models import Address, Inventory
from cart.models import Cart
from .forms import AdressForm


class user:
    @staticmethod
    def add_address(request):
        error, result = validade_cep(request.POST.get("cep"))
        if error:
            return error
        if result:
            form_copy = request.POST.copy()
            form_copy['tel'] = f"+55{request.POST.get("tel")}"
            form = AdressForm(form_copy)
                
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()
                return
            for campo, errors in form.errors.items():
                return errors[0]
        return "Cep Inválido"
            
    @staticmethod
    def create_inventory_and_cart(user):
        Inventory.objects.create(user=user)
        Cart.objects.create(user=user)
        return

    @staticmethod
    def delete_address(request):
        name = request.POST.get("name")
        address = get_object_or_404(Address, user=request.user, name=name)
        address.delete()
    

    staticmethod
    def get_orders(request):
        user = request.user
        orders = user.orders.all()
        return orders