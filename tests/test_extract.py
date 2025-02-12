from datetime import datetime, timedelta
import pandas as pd
import pytest
from src.extract import extract_ethereum_data, CoinGeckoAPIError
import requests
from unittest.mock import patch

def test_extract_ethereum_data_success():
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()
    df = extract_ethereum_data(start_date, end_date)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'date' in df.columns
    assert 'price' in df.columns
    assert df['date'].dtype == 'datetime64[ns, UTC]' # Corrigido: Verifica o tipo com UTC

def test_extract_ethereum_data_empty():
    start_date = datetime.now() + timedelta(days=30)
    end_date = datetime.now() + timedelta(days=60)
    df = extract_ethereum_data(start_date, end_date)
    assert isinstance(df, pd.DataFrame)
    assert df.empty

@patch('src.extract.requests.get')  # Mock da requisição
def test_extract_ethereum_data_api_error(mock_get):
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()

    # Simula um erro 401 da API
    mock_get.return_value.status_code = 401
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_get.return_value)

    with pytest.raises(CoinGeckoAPIError):
        extract_ethereum_data(start_date, end_date)

@patch('src.extract.requests.get')  # Mock da requisição
def test_extract_ethereum_data_request_error(mock_get):
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()

    # Simula um erro de requisição (ex: timeout)
    mock_get.side_effect = requests.exceptions.RequestException

    with pytest.raises(requests.exceptions.RequestException):
        extract_ethereum_data(start_date, end_date)