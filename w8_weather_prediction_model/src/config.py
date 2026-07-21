# W8 CONFIGURATION FILE

# GOAL: Central configuration file for the W8 Weather Prediction Model project.
# Purpose:
# - Store reusable project settings
# - Avoid hardcoded values across scripts
# - Improve maintainability and reproducibility

from pathlib import Path
import os


# Project Root


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Week 7 Feature Dataset


DEFAULT_DATA_PATH = (
    PROJECT_ROOT.parent
    / "w7_feature_engineering"
    / "data"
    / "processed"
    / "w7_features_final.parquet"
)

DATA_PATH = Path(
    os.getenv(
        "W7_FEATURE_DATA_PATH",
        str(DEFAULT_DATA_PATH)
    )
)


# Model Configuration


TARGET_COLUMN = "target_temp_next_hour"

RANDOM_STATE = 42

TEST_SIZE = 0.2


# Models Directory


MODEL_OUTPUT_DIR = PROJECT_ROOT / "models"

MODEL_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Saved Models


LINEAR_MODEL_PATH = (
    MODEL_OUTPUT_DIR
    / "linear_regression_model.pkl"
)

RANDOM_FOREST_MODEL_PATH = (
    MODEL_OUTPUT_DIR
    / "random_forest_model.pkl"
)

BEST_MODEL_PATH = (
    MODEL_OUTPUT_DIR
    / "best_model.pkl"
)

SCALER_PATH = (
    MODEL_OUTPUT_DIR
    / "scaler.pkl"
)


# Figures Directory


FIGURES_DIR = PROJECT_ROOT / "figures"

FIGURES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Model Comparison Figure


MODEL_COMPARISON_FIGURE = (
    FIGURES_DIR
    / "model_comparison.png"
)


# Feature Importance Figure


FEATURE_IMPORTANCE_FIGURE = (
    FIGURES_DIR
    / "feature_importance.png"
)


# Residual Comparison Figure


RESIDUAL_COMPARISON_FIGURE = (
    FIGURES_DIR
    / "residual_plot.png"
)


# Actual vs Predicted Figure


ACTUAL_VS_PREDICTED_FIGURE = (
    FIGURES_DIR
    / "actual_vs_predicted.png"
)


# Residual Distribution Figure


RESIDUAL_DISTRIBUTION_FIGURE = (
    FIGURES_DIR
    / "residual_distribution.png"
)


# Prediction Plot Figure (Future)


PREDICTION_PLOT_FIGURE = (
    FIGURES_DIR
    / "prediction_plot.png"
)