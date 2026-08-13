# The Code can run locally and as wll on airflow-pipeline to upload files to S3/cloud

import logging
import os
from pathlib import Path

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


if not AWS_REGION:
    raise RuntimeError("AWS_REGION is not configured.")

if not S3_BUCKET_NAME:
    raise RuntimeError("S3_BUCKET_NAME is not configured.")


s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    config=Config(
        retries={
            "max_attempts": 3,
            "mode": "standard",
        }
    ),
)


# W7 feature dataset

W7_FEATURE_FILE = Path(
    "w7_feature_engineering/data/processed/"
    "w7_features_final.parquet"
)

W7_S3_KEY = "features/w7_features_final.parquet"


# W8 model files

W8_MODEL_FILE = Path(
    "w8_weather_prediction_model/models/"
    "best_model.pkl"
)

W8_SCALER_FILE = Path(
    "w8_weather_prediction_model/models/"
    "scaler.pkl"
)

W8_METRICS_FILE = Path(
    "w8_weather_prediction_model/models/"
    "model_metrics.json"
)

W8_MODEL_S3_KEY = "models/best_model.pkl"
W8_SCALER_S3_KEY = "models/scaler.pkl"
W8_METRICS_S3_KEY = "models/model_metrics.json"


# W9 prediction file

W9_PREDICTION_FILE = Path(
    "w9_ml_pipeline/data/predictions/"
    "weather_predictions.csv"
)

W9_PREDICTION_S3_KEY = "predictions/weather_predictions.csv"


def upload_file(local_file, s3_key, description):
    """Upload one local file to S3."""

    local_file = Path(local_file)

    if not local_file.is_file():
        raise FileNotFoundError(
            f"{description} not found: {local_file}"
        )

    logger.info(
        "Uploading %s: %s",
        description,
        local_file,
    )

    logger.info(
        "S3 destination: s3://%s/%s",
        S3_BUCKET_NAME,
        s3_key,
    )

    try:
        s3_client.upload_file(
            str(local_file),
            S3_BUCKET_NAME,
            s3_key,
        )

    except ClientError as exc:
        logger.error(
            "%s upload failed: %s",
            description,
            exc,
        )

        raise RuntimeError(
            f"Failed to upload {description}."
        ) from exc

    s3_uri = (
        f"s3://{S3_BUCKET_NAME}/{s3_key}"
    )

    logger.info(
        "%s upload successful: %s",
        description,
        s3_uri,
    )

    return s3_uri


def upload_w7_features():
    """Upload the W7 feature dataset."""

    return upload_file(
        W7_FEATURE_FILE,
        W7_S3_KEY,
        "W7 feature dataset",
    )


def upload_w8_model():
    """Upload the W8 trained model."""

    return upload_file(
        W8_MODEL_FILE,
        W8_MODEL_S3_KEY,
        "W8 best model",
    )


def upload_w8_scaler():
    """Upload the W8 scaler."""

    return upload_file(
        W8_SCALER_FILE,
        W8_SCALER_S3_KEY,
        "W8 scaler",
    )


def upload_w8_metrics():
    """Upload the W8 model metrics."""

    return upload_file(
        W8_METRICS_FILE,
        W8_METRICS_S3_KEY,
        "W8 model metrics",
    )


def upload_w9_predictions():
    """Upload the W9 prediction CSV."""

    return upload_file(
        W9_PREDICTION_FILE,
        W9_PREDICTION_S3_KEY,
        "W9 prediction dataset",
    )

def upload_airflow_artifacts():
    """Upload selected W7-W9 artifacts from Airflow."""

    # W7 feature dataset
    upload_file(
        "/opt/airflow/w7/data/processed/w7_features_final.parquet",
        "features/w7_features_final.parquet",
        "W7 feature dataset",
    )

    # W8 best model
    upload_file(
        "/opt/airflow/w8/models/best_model.pkl",
        "models/best_model.pkl",
        "W8 best model",
    )

    # W8 scaler
    upload_file(
        "/opt/airflow/w8/models/scaler.pkl",
        "models/scaler.pkl",
        "W8 scaler",
    )

    # W8 model metrics
    upload_file(
        "/opt/airflow/w8/models/model_metrics.json",
        "models/model_metrics.json",
        "W8 model metrics",
    )

    # W9 predictions
    upload_file(
        "/opt/airflow/w9/data/predictions/weather_predictions.csv",
        "predictions/weather_predictions.csv",
        "W9 prediction dataset",
    )

    logger.info(
        "All selected W7-W9 artifacts uploaded successfully."
    )


if __name__ == "__main__":
    upload_w7_features()
    upload_w8_model()
    upload_w8_scaler()
    upload_w8_metrics()
    upload_w9_predictions()