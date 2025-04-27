# pipeline-airflow-case-Cadastra

Este projeto implementa uma pipeline ETL utilizando **Apache Airflow**, com coleta de dados de criptomoedas via API pública, armazenamento no **Supabase (PostgreSQL)** e criação de dashboard no **Power BI**.

## 📦 Funcionalidades
- Conexão com API pública de criptomoedas.
- Coleta de dados de **preço atual** e **histórico diário**.
- Armazenamento em banco de dados no Supabase (PostgreSQL).
- Atualização automática via DAGs no Airflow (6/6h e diária).
- Dashboard interativo em Power BI.

---

## ⚙️ Configuração do Ambiente

### Pré-requisitos
- Docker + Docker Compose
- Git
- Python 3.10+

### Clone o repositório
```bash
git clone https://github.com/guiosc/pipeline-airflow-case-Cadastra.git
cd pipeline-airflow-case-Cadastra
```

### Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
user=seu_usuario_postgres
password=sua_senha_postgres
host=seu_host_postgres
port=5432
dbname=seu_dbname
api_key=sua_api_key_crypto
```

---

## 🐳 Executando o Projeto com Docker

Suba o ambiente completo (Airflow + Dependências):
```bash
docker-compose up -d
```

O Airflow ficará disponível em:
```
http://localhost:8080
```

Usuário padrão:
- **Usuário:** airflow
- **Senha:** airflow

---

## 🚀 Executando o Pipeline

Após subir o ambiente:
1. Acesse o Airflow (`localhost:8080`)
2. Ative as DAGs:
   - `crypto_assets_etl` → Atualiza fatos e dimensão de cryptos.
   - `crypto_assets_history_etl` → Atualiza histórico de preços diários.
3. Rode manualmente a primeira execução ou aguarde o agendamento.

---

## 💄 Estrutura do Banco de Dados

O projeto cria e atualiza as seguintes tabelas:

- **dim_crypto** — Tabela de dimensão com dados das cryptos.
- **fact_assets** — Fato principal com dados atualizados (preço, market cap, etc).
- **fact_assets_history** — Histórico diário de preço para análise temporal.

<img href='https://github.com/guiosc/pipeline-airflow-case-Cadastra/blob/main/dashboard/tabelas-Supabase.png' width=100 px height=200>

---

## 📊 Dashboard no Power BI

Após populado o banco, conecte o **Power BI** no seu banco Postgres para construir visualizações como:
- Evolução do preço de Bitcoin, Ethereum, Dogecoin, etc.
- Quantidade de cryptos mapeadas.
- Melhor e pior performance diária de criptomoedas.

<img href='https://github.com/guiosc/pipeline-airflow-case-Cadastra/blob/main/dashboard/dashboard-Crypto.png' width=100 px height=200>

---

## 🧹 Boas práticas aplicadas

- Estrutura modularizada seguindo princípios de Clean Code.
- Isolamento de configuração via `.env`.
- Código comentado para facilitar manutenção.
- Upserts no banco para garantir consistência.
- Uso de logs no Airflow para rastreabilidade.

---

## 📄 Tecnologias utilizadas
- Apache Airflow
- Supabase (PostgreSQL)
- Docker & Docker Compose
- SQLAlchemy
- Pandas
- Power BI

---

## 🤝 Contribuição

Contribuições são bem-vindas!  
Sinta-se à vontade para abrir Issues ou Pull Requests.

---

## 🧐 Autor

Desenvolvido por [Guilherme Coelho](https://www.linkedin.com/in/guilherme-coelho-data-engineer/) no desafio de Data Engineering da Cadastra.

