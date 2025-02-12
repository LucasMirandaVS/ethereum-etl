from datetime import datetime
import pytz
import pandas as pd

def transform_ethereum_data(df):
    """
    Transforma os dados da Ethereum para o formato desejado.
    Recebe um DataFrame do pandas como entrada.
    """

    # Converte a coluna 'date' para datetime, se necessário
    if df['date'].dtype != 'datetime64[ns]':
        df['date'] = pd.to_datetime(df['date'])

    # Define o fuso horário para UTC, se necessário
    df['date'] = df['date'].dt.tz_localize('UTC', ambiguous='infer')

    return df