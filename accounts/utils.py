import requests

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