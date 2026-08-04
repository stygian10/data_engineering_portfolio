from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from src.check_archive import (
    determine_pipeline_branch,
    run_w1_w2_w3,
    run_w3_only,
)

from src.cleanup import cleanup_generated_files
from src.create_tables import create_table
from src.extract import extract_weather_data
from src.load import load_weather_data
from src.transform import transform_weather_data
from src.validate import validate_weather_data


default_args = {
    "owner": "portfolio_user",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def end_pipeline():
    print("\n===== Weather Intelligence Platform =====")
    print("Pipeline completed successfully.")
    print("=========================================\n")


with DAG(
    dag_id="weather_etl_pipeline",
    description="Weather Intelligence Platform",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=[
        "portfolio",
        "weather",
        "etl",
        "spark",
        "ml",
        "mlops",
    ],
) as dag:

    
    # PIPELINE STATE CHECK
    

    @task.branch(task_id="check_pipeline_state")
    def check_pipeline_state():
        return determine_pipeline_branch()


    pipeline_check = check_pipeline_state()


    
    # CREATE POSTGRES TABLE
    

    create_table_task = PythonOperator(
        task_id="create_postgresql_table",
        python_callable=create_table,
    )


    
    # RECOVERY TASKS
    

    run_all_recovery = PythonOperator(
        task_id="run_w1_w2_w3",
        python_callable=run_w1_w2_w3,
    )

    run_database_recovery = PythonOperator(
        task_id="run_w3_only",
        python_callable=run_w3_only,
    )

    skip_recovery = EmptyOperator(
        task_id="skip_recovery",
    )

    recovery_complete = EmptyOperator(
        task_id="recovery_complete",
        trigger_rule="none_failed_min_one_success",
    )


    
    # WEEK 4
    

    cleanup_task = PythonOperator(
        task_id="cleanup_generated_files",
        python_callable=cleanup_generated_files,
    )

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


    
    # WEEK 5
    

    spark_task = BashOperator(
        task_id="run_spark_etl",
        bash_command="""
        set -e
        cd /opt/airflow/w5
        python -m weather_etl.main
        """,
    )
        
    # WEEK 6
    

    upload_to_minio_task = BashOperator(
        task_id="upload_to_minio",
        bash_command="""
        set -e
        cd /opt/airflow/w6
        python -m src.upload_to_minio
        """,
    )

    
    # WEEK 7
    

    feature_engineering_task = BashOperator(
        task_id="run_feature_engineering",
        bash_command="""
        set -e
        cd /opt/airflow/w7
        python src/main.py
        """,
    )

    
    # WEEK 8
    

    model_training_task = BashOperator(
        task_id="run_model_training",
        bash_command="""
        set -e
        cd /opt/airflow/w8
        python src/compare_models.py
        """,
    )

    
    # WEEK 9
    

    prediction_pipeline_task = BashOperator(
        task_id="run_prediction_pipeline",
        bash_command="""
        set -e
        cd /opt/airflow/w9
        python src/main.py
        """,
    )

    upload_prediction_to_minio_task = BashOperator(
        task_id="upload_prediction_to_minio",
        bash_command="""
        set -e
        cd /opt/airflow/w9
        python src/upload_to_minio.py
        """,
    )

    
    # END
    

    end_task = PythonOperator(
        task_id="end_pipeline",
        python_callable=end_pipeline,
    )

    
    # PIPELINE FLOW
    

    create_table_task >> pipeline_check

    pipeline_check >> run_all_recovery
    pipeline_check >> run_database_recovery
    pipeline_check >> skip_recovery

    run_all_recovery >> recovery_complete
    run_database_recovery >> recovery_complete
    skip_recovery >> recovery_complete

    (
        recovery_complete
        >> cleanup_task
        >> extract_task
        >> transform_task
        >> load_task
        >> validate_task
        >> spark_task
        >> upload_to_minio_task
        >> feature_engineering_task
        >> model_training_task
        >> prediction_pipeline_task
        >> upload_prediction_to_minio_task
        >> end_task
    )
