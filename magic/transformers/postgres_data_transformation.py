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
    Extrae los datos de la tabla 'ventas', calcula métricas, y respeta los IDs originales
    evitando duplicar registros ya procesados.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    # 1. Obtener el último id procesado desde la tabla destino (detalle_ventas).
    # Se asume que en detalle_ventas se guarda el id original de ventas.
    last_id_query = 'SELECT COALESCE(MAX(id),0) as last_id FROM detalle_ventas;'
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        last_id_df = loader.load(last_id_query)
    last_id = int(last_id_df['last_id'].iloc[0])
    print(f"Último id procesado: {last_id}")

    # 2. Consulta SQL para extraer solo los registros nuevos de la tabla ventas.
    query = f'''
        SELECT *
        FROM ventas
        WHERE id > {last_id}
        ORDER BY id;
    '''

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        df = loader.load(query)

    if df.empty:
        print("No hay nuevos registros en ventas.")
        return df

    # Convertir tipos de datos correctamente.
    df['cantidad'] = df['cantidad'].astype(int)
    df['precio_unitario'] = df['precio_unitario'].astype(float)

    # Calcular el total de la venta.
    df['total_venta'] = df['cantidad'] * df['precio_unitario']

    # Clasificar ventas según el total.
    df['categoria_venta'] = df['total_venta'].apply(lambda total:
        'Alta' if total > 1000 else 'Media' if total >= 500 else 'Baja')

    # Convertir fecha a formato datetime y extraer mes de la venta.
    df['fecha_venta'] = pd.to_datetime(df['fecha_venta'])
    df['mes_venta'] = df['fecha_venta'].dt.month

    print(df)  # Para verificar los cambios

    return df

@test
def test_output(output, *args) -> None:
    """
    Pruebas para verificar la transformación de datos.
    """
    assert output is not None, 'El resultado de la transformación es None'
    # Se permite que el DataFrame esté vacío si no hay nuevos registros.
    if not output.empty:
        assert 'total_venta' in output.columns, 'La columna total_venta no fue generada'
        assert 'categoria_venta' in output.columns, 'La columna categoria_venta no fue generada'
        assert 'mes_venta' in output.columns, 'La columna mes_venta no fue generada'
        assert output['id'].is_unique, 'Los ID originales no son únicos, hay duplicados'
