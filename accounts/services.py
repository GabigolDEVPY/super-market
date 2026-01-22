from django.shortcuts import get_object_or_404
from .integrations.viacep import validade_cep
from django.core.exceptions import ValidationError
from .models import Address, Inventory
from django.contrib.auth import authenticate, login, logout
from cart.models import Cart
from django.db import transaction
from .forms import AdressForm


class User:
    
    @staticmethod
    @transaction.atomic
    def create_address(user, data):
        is_valid, error = validade_cep(data.get("cep"))
        if not is_valid:
            raise ValidationError(error)
        form_copy = data.copy()
        form_copy['tel'] = f"+55{data.get("tel")}"
            
        form = AdressForm(form_copy)
        if not form.is_valid():
            raise ValidationError(form.errors)
        address = form.save(commit=False)
        address.user = user
        address.save()
            
    @staticmethod
    def create_inventory_and_cart(user):
        Inventory.objects.create(user=user)
        Cart.objects.create(user=user)
        return

    @staticmethod
    def delete_address(request):
        address = get_object_or_404(Address, user=request.user, name=request.POST.get("name"))
        address.delete()

    @staticmethod
    def get_orders(request):
        return request.user.orders.all()
    
    @staticmethod
    def user_login(request):
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return
        return "error"
    
    @staticmethod
    def user_register(form):
        user_temp = form.save(commit=False)
        user_temp.save()
        User.create_inventory_and_cart(user_temp)
        return

    @staticmethod
    def change_password(request):
        user = request.user
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        if not user.check_password(old_password):
            return "error"
        user.set_password(new_password)
        user.save()
        
    @staticmethod
    def change_email(request):
        new_email = request.POST.get("email")
        if not new_email:
            return "error"
        request.user.email = new_email
        request.user.save()
