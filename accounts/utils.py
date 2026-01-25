import requests

def validade_cep(cep):
    cep = cep
    url= f"https://viacep.com.br/ws/{cep}/json/"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        result = response.json()
        return True, result
    except requests.exceptions.Timeout: 
        return "O servidor domorou pra responder", None
    except requests.exceptions.HTTPError as e:
        return "Cep inválido", None

