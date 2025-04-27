# DAG para atualizar fato_assets e dim_crypto (executa a cada 6 horas)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging
from src.api_client import get_data
from src.models import transformation_assets, transformation_dim_crypto
from src.db_manager import upsert_fact_assets, upsert_dim_crypto
from src.config import API_KEY

# Argumentos padrão da DAG
DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Função principal da ETL (extração, transformação e carga)
def extract_transform_load_assets():
    logging.info("Iniciando ETL de crypto assets...")

    # Requisição dos dados da API
    raw_assets = get_data("assets", params={"limit": 100, "apiKey": API_KEY})
    
    if raw_assets and "data" in raw_assets:
        logging.info(f"Dados extraídos: {len(raw_assets['data'])} registros.")

        # Transformação dos dados brutos
        df_assets = transformation_assets(raw_assets["data"])
        df_dim_crypto = transformation_dim_crypto(raw_assets["data"])

        logging.info(f"DataFrame df_assets: {df_assets.shape}")
        logging.info(f"DataFrame df_dim_crypto: {df_dim_crypto.shape}")

        # Inserção ou atualização nos bancos de dados
        upsert_dim_crypto(df_dim_crypto)
        upsert_fact_assets(df_assets)

        logging.info("ETL de crypto assets finalizado.")
    else:
        logging.warning("Falha ao extrair dados!")

# Definição da DAG
with DAG(
    dag_id="crypto_assets_etl",
    default_args=DEFAULT_ARGS,
    description="Atualiza fato_assets e dim_crypto",
    start_date=datetime(2025, 4, 26),
    schedule_interval="0 */6 * * *",
    catchup=False,
    tags=["crypto", "etl"]
) as dag:

    # Task responsável por executar a função de ETL
    task_extract_transform_load_assets = PythonOperator(
        task_id="extract_transform_load_assets",
        python_callable=extract_transform_load_assets
    )

    # Organização de dependência das tasks (nesse caso só uma)
    task_extract_transform_load_assets
