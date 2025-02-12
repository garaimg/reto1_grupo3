import pandas as pd
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform_sales_data(*args, **kwargs) -> DataFrame:
    """
    Cargar datos de la tabla ventas en PostgreSQL, calcular el total de la venta,
    categorizar las ventas y extraer el mes de la fecha de venta.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    # Consulta SQL para extraer los datos de la tabla ventas
    query = 'SELECT * FROM ventas ORDER BY fecha_venta DESC;'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    # Asegurar que las columnas sean del tipo correcto
    df['cantidad'] = df['cantidad'].astype(float)
    df['precio_unitario'] = df['precio_unitario'].astype(float)

    # Calcular el total de la venta
    df['total_venta'] = df['cantidad'] * df['precio_unitario']

    # Clasificar ventas según el total
    def categorizar_venta(total):
        if total > 1000:
            return 'Alta'
        elif total >= 500:
            return 'Media'
        return 'Baja'

    df['categoria_venta'] = df['total_venta'].apply(categorizar_venta)

    # Convertir fecha a formato datetime y extraer mes de la venta
    df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
    df['mes_venta'] = df['fecha_venta'].dt.month

    print(df)  # Para verificar que las nuevas columnas fueron agregadas

    return df

@test
def test_output(output, *args) -> None:
    """
    Pruebas para verificar la transformación de datos.
    """
    assert output is not None, 'El resultado de la transformación es None'
    assert not output.empty, 'No se encontraron datos de ventas'
    assert 'total_venta' in output.columns, 'La columna total_venta no fue generada'
    assert 'categoria_venta' in output.columns, 'La columna categoria_venta no fue generada'
    assert 'mes_venta' in output.columns, 'La columna mes_venta no fue generada'
