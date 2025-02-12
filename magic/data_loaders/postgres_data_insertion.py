import random
from datetime import datetime, timedelta
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

@data_loader
def load_data(*args, **kwargs):
    """
    Genera e inserta ventas aleatorias en la tabla ventas de PostgreSQL.
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    productos = ['Consola Retro', 'Joystick', 'Cartucho Clásico', 'Adaptador HDMI', 'Cargador USB']
    
    # Generar datos aleatorios de ventas en un DataFrame
    data = []
    for _ in range(10):  # Insertar 10 registros
        producto = random.choice(productos)
        cantidad = random.randint(1, 10)
        precio_unitario = round(random.uniform(10, 200), 2)  # Precio aleatorio entre 10 y 200
        fecha_venta = (datetime.now() - timedelta(days=random.randint(0, 30))).date()

        data.append([producto, cantidad, precio_unitario, fecha_venta])

    df = DataFrame(data, columns=['producto', 'cantidad', 'precio_unitario', 'fecha_venta'])

    # Conectar a PostgreSQL y exportar los datos
    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            'public',  # Esquema en PostgreSQL
            'ventas',  # Tabla de destino
            if_exists='append',  # Agregar nuevas filas sin sobrescribir
            index=False  # No incluir el índice de Pandas en la exportación
        )

    print("Datos insertados correctamente en la tabla ventas.")
    print(df)
