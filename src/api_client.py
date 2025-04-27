import requests
from requests.exceptions import RequestException

# Função para requisição via API
def get_data(path: str, params: dict=None) -> dict:
    url = f"https://rest.coincap.io/v3/{path}"

    # Passagem dos parâmetros
    if params:
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        url += f"?{query_string}"
    
    # Requisição e retorno em JSON
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except RequestException as e:
        print(f"[ERRO] Falha na requisição: {e}")
        return None
    