FROM apache/airflow:2.7.3-python3.10

WORKDIR /opt/airflow/

COPY . .

RUN pip install -r requirements.txt
