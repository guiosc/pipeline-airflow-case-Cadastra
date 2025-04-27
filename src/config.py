import os
from dotenv import load_dotenv

load_dotenv()

# Chave API
API_KEY=os.getenv("API_KEY")

# Variáveis de conexão com o banco
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

