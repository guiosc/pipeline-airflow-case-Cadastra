from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, MetaData
import os
from src.config import USER, HOST, PORT, PASSWORD, DBNAME
from dotenv import load_dotenv

# Carregando variáveis de ambiente
load_dotenv()

# URL de conexão com o banco de dados
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Criando engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Mapeando tabelas existentes no banco
metadata = MetaData()
fact_assets = Table('fact_assets', metadata, autoload_with=engine)
fact_assets_history = Table('fact_assets_history', metadata, autoload_with=engine)
dim_crypto = Table('dim_crypto', metadata, autoload_with=engine)


# Upsert para a dimensão de criptomoedas (dim_crypto)
def upsert_dim_crypto(df_dim_crypto):
    """
    Realiza upsert (insert ou update) dos dados na tabela dim_crypto.
    """
    with engine.begin() as connection:
        for index, row in df_dim_crypto.iterrows():
            stmt = insert(dim_crypto).values(
                crypto_id=row['crypto_id'],
                crypto_name=row['crypto_name'],
                symbol=row['symbol']
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['crypto_id'],
                set_={
                    "crypto_name": row['crypto_name'],
                    "symbol": row['symbol']
                }
            )
            connection.execute(stmt)


# Upsert para a tabela de fatos fact_assets (dados atuais das cryptos)
def upsert_fact_assets(df_fact_assets):
    """
    Realiza upsert (insert ou update) dos dados na tabela fact_assets.
    """
    with engine.begin() as connection:
        for index, row in df_fact_assets.iterrows():
            stmt = insert(fact_assets).values(
                crypto_id=row['crypto_id'],
                market_cap_usd=row['market_cap_usd'],
                max_supply=row['max_supply'],
                price_usd=row['price_usd'],
                rank=row['rank'],
                supply=row['supply'],
                updated_time=row['updated_time'],
                volume_usd_24h=row['volume_usd_24h'],
                change_percent_24h=row['change_percent_24h'],
                vwap24h=row['vwap24h']
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['crypto_id'],
                set_={
                    "market_cap_usd": row['market_cap_usd'],
                    "max_supply": row['max_supply'],
                    "price_usd": row['price_usd'],
                    "rank": row['rank'],
                    "supply": row['supply'],
                    "updated_time": row['updated_time'],
                    "volume_usd_24h": row['volume_usd_24h'],
                    "change_percent_24h": row['change_percent_24h'],
                    "vwap24h": row['vwap24h']
                }
            )
            connection.execute(stmt)


# Upsert para a tabela de fatos fact_assets_history (histórico de preços)
def upsert_fact_assets_history(df_fact_assets_history):
    """
    Realiza upsert (insert ou update) dos dados na tabela fact_assets_history.
    """
    with engine.begin() as connection:
        for index, row in df_fact_assets_history.iterrows():
            stmt = insert(fact_assets_history).values(
                crypto_id=row['crypto_id'],
                price_usd=row['price_usd'],
                date=row['date']
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['crypto_id', 'date'],
                set_={
                    "price_usd": row['price_usd'],
                    "date": row['date']
                }
            )
            connection.execute(stmt)
