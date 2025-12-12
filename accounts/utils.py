from django.shortcuts import redirect, render
import requests
from .models import Address
from .forms import AdressForm

def validade_cep(cep):
    cep = cep
    url= f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return (content := response.json())
    except requests.exceptions.Timeout: 
        return "Timeout"
    except requests.exceptions.HTTPError as e:
        return "Error"
    
def add_cep(request):
    if request.method == "POST":
        form_copy = request.POST.copy()
        form_copy['tel'] = f"+55{request.POST.get("tel")}"
        form = AdressForm(form_copy)
        
        if form.is_valid():
            print("válido")
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return form, (error := False)
        return form, (error := True)