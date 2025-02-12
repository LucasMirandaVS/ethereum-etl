import requests
from datetime import datetime, timedelta
import pytz
import pandas as pd
import os

class CoinGeckoAPIError(Exception):
    pass

def extract_ethereum_data(start_date, end_date, data_dir="data"):
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    base_url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range"
    all_data = []

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
            response.raise_for_status()

            json_data = response.json()

            if "prices" in json_data:
                for item in json_data["prices"]:
                    timestamp, price = item
                    date = datetime.fromtimestamp(timestamp / 1000, tz=pytz.utc)
                    all_data.append({"date": date, "price": price})
            else:
                print(f"A resposta da API não continha a chave 'prices': {json_data}")

        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            if isinstance(e, requests.exceptions.HTTPError):
                print(f"Código de status do erro: {e.response.status_code}")
                if e.response.status_code == 401:
                    raise CoinGeckoAPIError("Erro de autenticação na API CoinGecko")
                raise # Re-lança exceções HTTP
            raise  # Re-lança outras exceções de requisição
        except CoinGeckoAPIError as e:
            print(f"Erro na API CoinGecko: {e}")
            return pd.DataFrame()
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return pd.DataFrame()

        current_date = to_date + timedelta(days=1)

    df = pd.DataFrame(all_data)
    return df