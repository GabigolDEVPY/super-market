from django.shortcuts import get_object_or_404
from .integrations.viacep import validade_cep
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .models import Address, Inventory
from django.contrib.auth import authenticate, login
from cart.models import Cart
from django.db import transaction
from .forms import AdressForm

class AddressService:
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
    def delete_address(user, name):
        Address.objects.get(user=user, name=name).delete()


class UserService:
    
    @staticmethod
    def get_orders(user):
        return user.orders.all()
    

    @staticmethod
    def change_email(email, user):
        user.email = email
        user.save()

        
class AuthService:
    
    @staticmethod
    def user_login(request, username, password):
        user = authenticate(request, username=username, password=password)
        if not user:
            raise ValidationError("Usuário ou senha Inválidos")
        login(request, user)
    
    
    @staticmethod
    @transaction.atomic
    def user_register(form):
        user_temp = form.save()
        Inventory.objects.create(user=user_temp)
        Cart.objects.create(user=user_temp)

    
    @staticmethod
    def change_password(user, old_password, new_password):
        if not user.check_password(old_password):
            raise ValidationError("Senha não coincide")
        user.set_password(new_password)
        user.save()