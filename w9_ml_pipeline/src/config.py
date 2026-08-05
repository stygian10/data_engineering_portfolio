from pathlib import Path
import os


# =====================================================
# Project Root
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# =====================================================
# Detect Environment
# =====================================================

AIRFLOW_ROOT = Path("/opt/airflow")

if AIRFLOW_ROOT.exists():

    PORTFOLIO_ROOT = AIRFLOW_ROOT

    W7_FOLDER = "w7"
    W8_FOLDER = "w8"

else:

    PORTFOLIO_ROOT = PROJECT_ROOT.parent

    W7_FOLDER = "w7_feature_engineering"
    W8_FOLDER = "w8_weather_prediction_model"


# =====================================================
# Week 7 Feature Dataset
# =====================================================

DEFAULT_FEATURE_DATA_PATH = (
    PORTFOLIO_ROOT
    / W7_FOLDER
    / "data"
    / "processed"
    / "w7_features_final.parquet"
)

FEATURE_DATA_PATH = Path(
    os.getenv(
        "W7_FEATURE_DATA_PATH",
        str(DEFAULT_FEATURE_DATA_PATH),
    )
)


# =====================================================
# Week 8 Model Files
# =====================================================

DEFAULT_BEST_MODEL_PATH = (
    PORTFOLIO_ROOT
    / W8_FOLDER
    / "models"
    / "best_model.pkl"
)

BEST_MODEL_PATH = Path(
    os.getenv(
        "W8_BEST_MODEL_PATH",
        str(DEFAULT_BEST_MODEL_PATH),
    )
)


DEFAULT_SCALER_PATH = (
    PORTFOLIO_ROOT
    / W8_FOLDER
    / "models"
    / "scaler.pkl"
)

SCALER_PATH = Path(
    os.getenv(
        "W8_SCALER_PATH",
        str(DEFAULT_SCALER_PATH),
    )
)


# =====================================================
# Output Directories
# =====================================================

DEFAULT_OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "predictions"
)

OUTPUT_DIR = Path(
    os.getenv(
        "W9_OUTPUT_DIR",
        str(DEFAULT_OUTPUT_DIR),
    )
)


DEFAULT_FIGURES_DIR = (
    PROJECT_ROOT
    / "figures"
)

FIGURES_DIR = Path(
    os.getenv(
        "W9_FIGURES_DIR",
        str(DEFAULT_FIGURES_DIR),
    )
)


DEFAULT_LOG_DIR = (
    PROJECT_ROOT
    / "logs"
)

LOG_DIR = Path(
    os.getenv(
        "W9_LOG_DIR",
        str(DEFAULT_LOG_DIR),
    )
)


# =====================================================
# Prediction Output Files
# =====================================================

PREDICTION_CSV = (
    OUTPUT_DIR
    / os.getenv(
        "W9_PREDICTION_CSV",
        "weather_predictions.csv",
    )
)

PREDICTION_PARQUET = (
    OUTPUT_DIR
    / os.getenv(
        "W9_PREDICTION_PARQUET",
        "weather_predictions.parquet",
    )
)


# =====================================================
# Evaluation Figures
# =====================================================

PREDICTION_VS_ACTUAL_FIGURE = (
    FIGURES_DIR
    / "prediction_vs_actual.png"
)

RESIDUAL_PLOT_FIGURE = (
    FIGURES_DIR
    / "residual_plot.png"
)

ERROR_DISTRIBUTION_FIGURE = (
    FIGURES_DIR
    / "error_distribution.png"
)


# =====================================================
# Prediction Configuration
# =====================================================

TARGET_COLUMN = "target_temp_next_hour"

PREDICTION_COLUMN = "predicted_temperature"

TIME_COLUMN = "time"


# =====================================================
# MinIO Configuration
# =====================================================

MINIO_ENDPOINT = os.getenv(
    "MINIO_ENDPOINT",
    "localhost:9000",
)

MINIO_ACCESS_KEY = os.getenv(
    "MINIO_ACCESS_KEY",
    "minioadmin",
)

MINIO_SECRET_KEY = os.getenv(
    "MINIO_SECRET_KEY",
    "minioadmin",
)

MINIO_SECURE = (
    os.getenv(
        "MINIO_SECURE",
        "False",
    ).lower()
    == "true"
)

MINIO_BUCKET_NAME = os.getenv(
    "MINIO_BUCKET_NAME",
    "weather-data-lake",
)

MINIO_PREFIX = os.getenv(
    "MINIO_PREFIX",
    "predictions/",
)


# =====================================================
# Create Required Directories
# =====================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)