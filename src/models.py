import pandas as pd
from datetime import datetime, timezone

# Fato cryto
def transformation_assets(raw_data: list[dict]) -> pd.DataFrame:
    # Lendo o json e transformando em df
    df = pd.json_normalize(raw_data)
    df = df[[
        "id",
        "rank",
        "supply",
        "maxSupply",
        "marketCapUsd",
        "volumeUsd24Hr",
        "priceUsd",
        "changePercent24Hr",
        "vwap24Hr"
    ]]

    # Renomeando colunas
    df = df.rename(columns={
        "id": "crypto_id",
        "maxSupply": "max_supply",
        "marketCapUsd": "market_cap_usd",
        "volumeUsd24Hr": "volume_usd_24h",
        "priceUsd": "price_usd",
        "changePercent24Hr": "change_percent_24h",
        "vwap24Hr": "vwap24h"

    })

    # Tipagem dos campos
    df["crypto_id"] = df["crypto_id"].astype(str)
    df["rank"] = df["rank"].astype(int)
    df["supply"] = pd.to_numeric(df["supply"], errors="coerce")
    df["max_supply"] = pd.to_numeric(df["max_supply"], errors="coerce")
    df["market_cap_usd"] = pd.to_numeric(df["market_cap_usd"], errors="coerce")
    df["volume_usd_24h"] = pd.to_numeric(df["volume_usd_24h"], errors="coerce")
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    df["change_percent_24h"] = pd.to_numeric(df["change_percent_24h"], errors="coerce")
    df["vwap24h"] = pd.to_numeric(df["vwap24h"], errors="coerce")
    
    # Adicionando uma coluna do horário
    df["updated_time"] = datetime.now(timezone.utc)

    return df


# Fato histórico
def transformation_assets_history(raw_data: list[dict], crypto_id: str) -> pd.DataFrame:
    # Lendo o json e transformando em df
    df = pd.json_normalize(raw_data)
    
    # Renomeando colunas
    df = df[["priceUsd", "date"]]
    df = df.rename(columns={"priceUsd": "price_usd"})
    
    # Tipagem dos campos
    df["crypto_id"] = crypto_id
    df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    
    df = df[["crypto_id", "price_usd", "date"]]
    
    return df


# Criando a dimensão das Cryptos
def transformation_dim_crypto(raw_data: list[dict]) -> pd.DataFrame:
    # Lendo o json e transformando em df
    df = pd.json_normalize(raw_data)

    df = df[["id", "name", "symbol"]]
    # Renomeando colunas
    df = df.rename(columns={
        "id": "crypto_id",
        "name": "crypto_name",
    })
    # Tipagem dos campos
    df["crypto_id"] = df["crypto_id"].astype(str)
    df["crypto_name"] = df["crypto_name"].astype(str)
    df["symbol"] = df["symbol"].astype(str)

    return df