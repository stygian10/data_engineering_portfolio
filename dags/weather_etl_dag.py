from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

from orchestration.check_archive import (
    determine_pipeline_branch,
    run_w1_w2_w3,
    archive_expired_forecasts,
)

from orchestration.create_db import create_table
from orchestration.cloud_storage import upload_airflow_artifacts


# =====================================================
# DEFAULT ARGUMENTS
# =====================================================

default_args = {
    "owner": "portfolio_user",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


# =====================================================
# PROJECT PATHS
# =====================================================

W4_PATH = "/opt/airflow/w4"
W5_PATH = "/opt/airflow/w5"
W6_PATH = "/opt/airflow/w6"
W7_PATH = "/opt/airflow/w7"
W8_PATH = "/opt/airflow/w8"
W9_PATH = "/opt/airflow/w9"


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def create_project_task(
    task_id: str,
    project_dir: str,
    module: str,
):
    """
    Execute an independent project using its main module.
    """

    return BashOperator(
        task_id=task_id,
        bash_command=f"""
        set -e
        cd {project_dir}
        python -m {module}
        """,
    )


def end_pipeline():
    """
    Final pipeline message.
    """

    print("\n============================================")
    print("Weather Intelligence Platform Completed")
    print("============================================\n")


def refresh_applications():
    """
    Restart FastAPI and Prediction Dashboard deployments
    so their init containers download the latest S3 artifacts.
    """

    from datetime import datetime, timezone

    from kubernetes import client, config

    # Load Kubernetes credentials from inside the Airflow pod.
    config.load_incluster_config()

    apps = client.AppsV1Api()

    deployments = [
        "fastapi-deployment",
        "prediction-dashboard-deployment",
    ]

    for deployment_name in deployments:
        deployment = apps.read_namespaced_deployment(
            name=deployment_name,
            namespace="default",
        )

        annotations = (
            deployment.spec.template.metadata.annotations or {}
        )

        annotations["kubectl.kubernetes.io/restartedAt"] = (
            datetime.now(timezone.utc).isoformat()
        )

        deployment.spec.template.metadata.annotations = annotations

        apps.patch_namespaced_deployment(
            name=deployment_name,
            namespace="default",
            body=deployment,
        )

        print(
            f"[REFRESH] Restart triggered: {deployment_name}"
        )


# =====================================================
# DAG
# =====================================================

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

    # =================================================
    # DATABASE INITIALIZATION
    # =================================================

    create_database_task = PythonOperator(
        task_id="create_postgresql_table",
        python_callable=create_table,
    )

    # =================================================
    # PIPELINE RECOVERY CHECK
    # =================================================

    @task.branch(task_id="check_pipeline_state")
    def check_pipeline_state():
        return determine_pipeline_branch()

    pipeline_check = check_pipeline_state()

    # =================================================
    # RECOVERY TASKS
    # =================================================

    run_all_recovery = PythonOperator(
        task_id="run_w1_w2_w3",
        python_callable=run_w1_w2_w3,
    )

    skip_recovery = EmptyOperator(
        task_id="skip_recovery",
    )

    recovery_complete = EmptyOperator(
        task_id="recovery_complete",
        trigger_rule="none_failed_min_one_success",
    )

    # =================================================
    # FORECAST -> ARCHIVE TRANSITION
    # =================================================

    archive_forecast_transition = PythonOperator(
        task_id="archive_expired_forecasts",
        python_callable=archive_expired_forecasts,
    )

    # =================================================
    # WEEK 4
    # =================================================

    run_w4_pipeline = create_project_task(
        task_id="run_w4_pipeline",
        project_dir=W4_PATH,
        module="src.main",
    )

    # =================================================
    # WEEK 5
    # =================================================

    run_w5_pipeline = create_project_task(
        task_id="run_w5_pipeline",
        project_dir=W5_PATH,
        module="weather_etl.main",
    )

    # =================================================
    # WEEK 6
    # =================================================

    run_w6_pipeline = create_project_task(
        task_id="run_w6_pipeline",
        project_dir=W6_PATH,
        module="src.main",
    )

    # =================================================
    # WEEK 7
    # =================================================

    run_w7_pipeline = create_project_task(
        task_id="run_w7_pipeline",
        project_dir=W7_PATH,
        module="src.main",
    )

    # =================================================
    # WEEK 8
    # =================================================

    run_w8_pipeline = create_project_task(
        task_id="run_w8_pipeline",
        project_dir=W8_PATH,
        module="src.main",
    )

    # =================================================
    # WEEK 9
    # =================================================

    run_w9_pipeline = create_project_task(
        task_id="run_w9_pipeline",
        project_dir=W9_PATH,
        module="src.main",
    )

    upload_prediction_to_minio = create_project_task(
        task_id="upload_prediction_to_minio",
        project_dir=W9_PATH,
        module="src.upload_to_minio",
    )

    # =================================================
    # CLOUD STORAGE
    # =================================================

    upload_artifacts_to_s3 = PythonOperator(
        task_id="upload_artifacts_to_s3",
        python_callable=upload_airflow_artifacts,
    )

    # =================================================
    # REFRESH APPLICATIONS
    # =================================================

    refresh_applications_task = PythonOperator(
        task_id="refresh_applications",
        python_callable=refresh_applications,
    )

    # =================================================
    # END PIPELINE
    # =================================================

    end_task = PythonOperator(
        task_id="end_pipeline",
        python_callable=end_pipeline,
    )

    # =================================================
    # PIPELINE FLOW
    # =================================================

    # Database must exist before archive checking.
    create_database_task >> pipeline_check

    # -------------------------------------------------
    # Recovery branch
    # -------------------------------------------------

    pipeline_check >> run_all_recovery
    pipeline_check >> skip_recovery

    run_all_recovery >> recovery_complete
    skip_recovery >> recovery_complete

    # -------------------------------------------------
    # Forecast -> Archive transition
    #
    # ALWAYS runs after recovery/skip and before W4.
    # -------------------------------------------------

    recovery_complete >> archive_forecast_transition

    # -------------------------------------------------
    # Main pipeline
    # -------------------------------------------------

    (
        archive_forecast_transition
        >> run_w4_pipeline
        >> run_w5_pipeline
        >> run_w6_pipeline
        >> run_w7_pipeline
        >> run_w8_pipeline
        >> run_w9_pipeline
        >> upload_prediction_to_minio
        >> upload_artifacts_to_s3
        >> refresh_applications_task
        >> end_task
    )