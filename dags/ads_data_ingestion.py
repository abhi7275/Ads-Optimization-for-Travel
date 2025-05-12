from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DATABASE_URI = 'postgresql+psycopg2://admin:admin@postgres-db:5432/ads_db'

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 5, 13),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ads_data_ingestion',
    default_args=default_args,
    description='Ingest Ads Data into PostgreSQL',
    schedule_interval='@daily',
)

# Data ingestion function
def ingest_data():
    # Load the dataset from CSV
    file_path = '/opt/airflow/dags/data.csv'  # Path inside Docker container
    df = pd.read_csv(file_path)

    # Connect to PostgreSQL
    engine = create_engine(DATABASE_URI)
    connection = engine.connect()

    # Insert data into the table
    df.to_sql('ads_performance', con=connection, if_exists='replace', index=False)

    # Close the connection
    connection.close()
    print("Data successfully ingested into PostgreSQL.")

# Define the Airflow task
ingestion_task = PythonOperator(
    task_id='ingest_ads_data',
    python_callable=ingest_data,
    dag=dag,
)

ingestion_task
