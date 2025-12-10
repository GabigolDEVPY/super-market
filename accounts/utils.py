import requests
from .models import Address

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
    data = request.POST.dict()
    add_adress = Address.objects.create(
        user = request.user,
        address =data["address"], 
        complement =data["complement"],
        neighborhood =data["neighborhood"],
        number=data["number"],
        tel=data["tel"],
        city=data["city"],
        cep=data["cep"],
        state=data["state"] 
    )
    