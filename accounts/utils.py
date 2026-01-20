from django.shortcuts import redirect, render, get_object_or_404
import requests
from payment.models import Order
from .models import Address, Inventory
from cart.models import Cart
from .forms import AdressForm

def validade_cep(cep):
    cep = cep
    url= f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        result = response.json()
        return None, result
    except requests.exceptions.Timeout: 
        return "O servidor domorou pra responder", None
    except requests.exceptions.HTTPError as e:
        return "Cep inválido", None

