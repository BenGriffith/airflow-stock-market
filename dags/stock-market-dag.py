from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, date
from airflow.utils.dates import days_ago
import yfinance as yf
import pandas as pd
import requests

default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'marketvol',
    default_args=default_args,
    description='Stock Market DAG for AAPL and TSLA',
    schedule_interval='0 18 * * 1-5', # Only runs on weekdays (M to F)
    start_date=days_ago(1) # 6 PM on current date
)

t0 = BashOperator(
    task_id='create_directory',
    bash_command="mkdir -p /usr/local/spark/resources/data/tmp/{{ ds }}",
    dag=dag
)


def get_stock_data(stock):
    start_date = date.today() - timedelta(days=1)
    end_date = date.today() 
    df = yf.download(stock, start=start_date, end=end_date, interval='1m')
    df.to_csv('/usr/local/spark/resources/data/tmp/{}/{}-data.csv'.format(end_date.strftime("%Y-%m-%d"), stock.lower()), header=False)


t1 = PythonOperator(
    task_id='get_apple_data',
    python_callable=get_stock_data,
    op_kwargs={'stock': 'AAPL'},
    dag=dag
)

t2 = PythonOperator(
    task_id='get_tesla_data',
    python_callable=get_stock_data,
    op_kwargs={'stock': 'TSLA'},
    dag=dag
)

t3 = BashOperator(
    task_id='move_apple',
    bash_command="mv /usr/local/spark/resources/data/tmp/{{ ds }}/aapl-data.csv /usr/local/spark/resources/data/query/",
    dag=dag
)

t4 = BashOperator(
    task_id='move_tesla',
    bash_command="mv /usr/local/spark/resources/data/tmp/{{ ds }}/tsla-data.csv /usr/local/spark/resources/data/query/",
    dag=dag
)


def query():
    apple_df = pd.read_csv('/usr/local/spark/resources/data/query/aapl-data.csv')
    tesla_df = pd.read_csv('/usr/local/spark/resources/data/query/tsla-data.csv')
    print(apple_df.head())
    print(tesla_df.head())


t5 = PythonOperator(
    task_id='query_data',
    python_callable=query,
    dag=dag
)

t0 >> t1 >> t3
t0 >> t2 >> t4
[t3, t4] >> t5