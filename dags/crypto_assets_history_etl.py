# DAG para inserir valores históricos na fact_assets_history

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.api_client import get_data
from src.models import transformation_assets_history
from src.db_manager import upsert_fact_assets_history
from src.config import API_KEY
import logging

# Argumentos padrão da DAG
DEFAULT_ARGS = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Função principal da ETL de histórico de preços
def extract_transform_load_assets_history():
    # Lista das 5 principais criptomoedas a serem coletadas
    crypto_ids = ["bitcoin", "ethereum", "tether", "binance-coin", "dogecoin"]
    
    for crypto_id in crypto_ids:
        logging.info(f"Extraindo histórico para {crypto_id}...")
        
        # Requisição dos dados históricos via API
        raw_history = get_data(f"assets/{crypto_id}/history", params={"interval": "d1", "apiKey": API_KEY})
        
        if raw_history and "data" in raw_history:
            logging.info(f"Dados históricos extraídos para {crypto_id}: {len(raw_history['data'])} registros.")

            # Transformação dos dados brutos
            df_history = transformation_assets_history(raw_history["data"], crypto_id=crypto_id)
            logging.info(f"DataFrame df_history ({crypto_id}): {df_history.shape}")
            
            # Inserção ou atualização no banco de dados
            upsert_fact_assets_history(df_history)
        else:
            logging.warning(f"Falha ao extrair histórico de {crypto_id}.")

# Definição da DAG
with DAG(
    dag_id="crypto_assets_history_etl",
    default_args=DEFAULT_ARGS,
    description="Insere histórico diário das 5 maiores cryptos",
    start_date=datetime(2025, 4, 26),
    schedule_interval="@daily", 
    catchup=False,                 
    tags=["crypto", "history"]     
) as dag:

    # Task responsável por executar a função de ETL histórica
    task_extract_transform_load_assets_history = PythonOperator(
        task_id="extract_transform_load_assets_history",
        python_callable=extract_transform_load_assets_history
    )

    task_extract_transform_load_assets_history
