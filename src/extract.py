import requests
from datetime import datetime, timedelta
import pytz

class CoinGeckoAPIError(Exception):
    pass

def extract_ethereum_data(start_date, end_date):
    """
    Extrai dados da Ethereum da API CoinGecko, incluindo a data.
    """
    base_url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range"
    data = []

    current_date = start_date
    while current_date <= end_date:
        to_date = min(current_date + timedelta(days=365), end_date)
        from_ts = int(current_date.timestamp())
        to_ts = int(to_date.timestamp())

        params = {
            "vs_currency": "usd",
            "from": from_ts,
            "to": to_ts
        }

        try:
            response = requests.get(base_url, params=params)
            print(f"URL da requisição: {response.url}")
            print(f"Código de status: {response.status_code}")
            print(f"Conteúdo da resposta: {response.text}")
            if response.status_code == 401:
                raise CoinGeckoAPIError("Erro de autenticação na API CoinGecko")
            response.raise_for_status()
            json_data = response.json()
            if "prices" in json_data:
                for item in json_data["prices"]:
                    timestamp, price = item
                    date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)  # Adiciona fuso horário UTC
                    data.append({"date": date, "price": price})  # Inclui data e preço
            else:
                print(f"A resposta da API não continha a chave 'prices': {json_data}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            print(f"Tipo da exceção: {type(e)}")
            if isinstance(e, requests.exceptions.HTTPError):
                raise
        except CoinGeckoAPIError as e:
            print(f"Erro na API CoinGecko: {e}")
            return []

        current_date = to_date + timedelta(days=1)

    return data

if __name__ == "__main__":
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    ethereum_data = extract_ethereum_data(start_date, end_date)
    print(f"Dados extraídos: {len(ethereum_data)} registros")
    # Imprime os primeiros 5 registros para visualizar os dados com a data
    for i in range(min(5, len(ethereum_data))):
        print(ethereum_data[i])