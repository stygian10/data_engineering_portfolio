from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from tasks.extract_weather import extract_weather_data
from tasks.transform_weather import transform_weather_data
from tasks.load_weather import load_weather_data
from tasks.validate_weather import validate_weather_data


default_args = {
    "owner": "portfolio_user",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def end_pipeline():
    print("[END] Weather ETL pipeline finished successfully")


with DAG(
    dag_id="weather_etl_pipeline",
    description="Portfolio-ready multi-city ETL pipeline for weather data",
    default_args=default_args,
    start_date=datetime(2026, 3, 24),
    schedule="@daily",
    catchup=False,
    tags=["portfolio", "etl", "weather"],
) as dag:

   
    extract_task = PythonOperator(
        task_id="extract_weather_data",
        python_callable=extract_weather_data,
    )

    transform_task = PythonOperator(
        task_id="transform_weather_data",
        python_callable=transform_weather_data,
    )

    load_task = PythonOperator(
        task_id="load_weather_data",
        python_callable=load_weather_data,
    )

    validate_task = PythonOperator(
        task_id="validate_weather_data",
        python_callable=validate_weather_data,
    )

    # ------------------------
    # W5 Spark Task
    # ------------------------
    spark_task = BashOperator(
        task_id="run_spark_etl",
        bash_command="python /opt/airflow/w5/src/main.py",
    )

    # ------------------------
    # W6 MinIO Upload Task
    # ------------------------
    upload_to_minio_task = BashOperator(
        task_id="upload_to_minio",
        bash_command="python /opt/airflow/w6/scripts/upload_to_minio.py",
    )

    # ------------------------
    # W7 Feature Engineering Task
    # ------------------------

    feature_engineering_task = BashOperator(
        task_id="run_feature_engineering",
        bash_command="python /opt/airflow/w7/src/pipeline.py",
    )

    # ------------------------
    # End Task
    # ------------------------
    end_task = PythonOperator(
        task_id="end_pipeline",
        python_callable=end_pipeline,
    )

    # ------------------------
    # FINAL PIPELINE FLOW
    # ------------------------
    (
        extract_task
        >> transform_task
        >> load_task
        >> validate_task
        >> spark_task
        >> upload_to_minio_task
        >> feature_engineering_task
        >> end_task
    )