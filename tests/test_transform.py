from datetime import datetime
import pandas as pd
from src.transform import transform_ethereum_data

def test_transform_ethereum_data():
    data = {'date': [datetime(2024, 1, 1), datetime(2024, 1, 2)], 'price': [100.0, 110.0]}
    df = pd.DataFrame(data)
    transformed_df = transform_ethereum_data(df)

    assert isinstance(transformed_df, pd.DataFrame)
    assert not transformed_df.empty

    # Verifica se o tipo da coluna 'date' é datetime64[ns, UTC]
    assert transformed_df['date'].dtype == 'datetime64[ns, UTC]' # Mudança aqui