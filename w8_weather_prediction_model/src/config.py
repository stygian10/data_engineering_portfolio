# W8 CONFIGURATION FILE 

#GOALS: Central configuration file for the W8, Weather Prediction Model project.

# Purpose: Store reusable project settings, Avoid hardcoded values across scripts, Improve maintainability and reproducibility

# This file defines: dataset locations, target variable, train/test split settings, random seed, model save path

# Path to engineered parquet dataset
DATA_PATH = "data/raw/w7_features_final.parquet"

# Target column to predict
TARGET_COLUMN = "target_temp_next_day"

# Random seed for reproducibility
RANDOM_STATE = 42

# Train-test split ratio
TEST_SIZE = 0.2

# Model save path
MODEL_OUTPUT_PATH = "models/baseline_linear_regression.pkl"