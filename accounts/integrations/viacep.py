import requests

def validade_cep(cep):
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=3)
        response.raise_for_status()
        data = response.json()
        if data.get("erro"):
            return False, "CEP não encontrado"
        return True, data
    
    except requests.Timeout:
        return False, "Serviço de CEP indisponível"
    except requests.RequestException:
        return False, "Erro ao validar CEP"
