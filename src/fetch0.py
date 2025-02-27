from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, Field
import json
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# URL da API de Produção para obter a última cotação do Bitcoin
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

# Parâmetros da requisição para obter a cotação do Bitcoin
parameters = {
    'symbol': 'ETH',  # Identificando o Ethereum pelo símbolo
    'convert': 'BRL'  # Convertendo a cotação para BRL
}

# Headers com a chave da API obtida do arquivo .env
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv('CMC_API_KEY'),  # Obtendo a chave do .env
}

# Criar uma sessão
session = Session()
session.headers.update(headers)

# Modelo Pydantic para o Parsing da Resposta
class QuoteModel(BaseModel):
    price: float
    volume_24h: float = Field(alias='volume_24h')
    market_cap: float = Field(alias='market_cap')
    last_updated: str = Field(alias='last_updated')

class BitcoinDataModel(BaseModel):
    symbol: str
    quote: dict

    def get_brl_quote(self) -> QuoteModel:
        return QuoteModel(**self.quote['BRL'])

class ApiResponseModel(BaseModel):
    data: dict
    status: dict

    def get_ethereum_data(self) -> BitcoinDataModel:
        return BitcoinDataModel(**self.data['ETH'])

# Função que faz a requisição à API e processa os dados usando Pydantic
def consultar_cotacao_ethereum():
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        
        # Parsing da resposta usando Pydantic
        api_response = ApiResponseModel(**data)
        ethereum_data = api_response.get_ethereum_data()
        quote = ethereum_data.get_brl_quote()

        # Imprimir os dados da cotação
        print(f"Última cotação do Ethereum: ${quote.price:.2f} Reais")
        print(f"Volume 24h: ${quote.volume_24h:.2f} Reais")
        print(f"Market Cap: ${quote.market_cap:.2f} Reais")
        print(f"Última atualização: {quote.last_updated}")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"Erro na requisição: {e}")
    except ValidationError as e:
        print(f"Erro ao validar a resposta da API: {e}")

# Executa a função para consultar a cotação do Bitcoin
consultar_cotacao_ethereum()