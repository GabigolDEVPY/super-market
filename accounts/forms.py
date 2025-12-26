from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
class AdressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "name": "Nome",
            "address": "Endereço",
            "tel": "Telefone",
            "city": "Cidade",
            "neighborhood": "Bairro",
            "complement": "Complemento",
            "state": "Estado",
            "number": "Número",
            "cep": "Cep"
        }