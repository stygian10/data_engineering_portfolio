# W8 CONFIGURATION FILE 

#GOAL: Central configuration file for the W8, Weather Prediction Model project.

# Purpose: Store reusable project settings, Avoid hardcoded values across scripts, Improve maintainability and reproducibility

# This file defines: dataset locations, target variable, train/test split settings, random seed, model save path
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


TARGET_COLUMN = "target_temp_next_day"

RANDOM_STATE = 42

TEST_SIZE = 0.2


# Models Directory


MODEL_OUTPUT_DIR = PROJECT_ROOT / "models"

MODEL_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# Default model path
# (compare_models.py can overwrite this dynamically
# with linear_regression_model.pkl or
# random_forest_model.pkl)

MODEL_OUTPUT_PATH = (
    MODEL_OUTPUT_DIR
    / "best_model.pkl"
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

# Residual Plot (Future)

RESIDUAL_COMPARISON_FIGURE = (
    FIGURES_DIR
    / "residual_plot.png"
)

# Prediction Plot (Future)

PREDICTION_PLOT_FIGURE = (
    FIGURES_DIR
    / "prediction_plot.png"
)
