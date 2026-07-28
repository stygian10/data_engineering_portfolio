# W8 - MODEL COMPARISON SCRIPT
# Goal: Train multiple regression models, compare their
# performance, select the best model, and save all
# artifacts required for prediction and deployment.
#===================================================
# This script:
# Loads and preprocesses the Week 7 feature dataset
# Splits the data into training and testing sets
# Scales numerical features
# Trains Linear Regression and Random Forest models
# Evaluates both models using MAE, RMSE and R²
# Compares model performance
# Selects and saves the best-performing model
# Saves the trained models and scaler
# Generates evaluation figures
# Stores model metrics for the dashboard and API
import json
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from config import (
    DATA_PATH,
    TARGET_COLUMN,
    RANDOM_STATE,
    TEST_SIZE,
    MODEL_OUTPUT_DIR,
    LINEAR_MODEL_PATH,
    RANDOM_FOREST_MODEL_PATH,
    BEST_MODEL_PATH,
    SCALER_PATH,
    MODEL_METRICS_PATH,
    MODEL_COMPARISON_FIGURE,
    FEATURE_IMPORTANCE_FIGURE,
    RESIDUAL_COMPARISON_FIGURE
)


# LOAD DATASET

print("Loading dataset...")

df = pd.read_parquet(DATA_PATH)

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())


# PREPARE FEATURES & TARGET

print("\nPreparing dataset...")

df = df.dropna()

X = df.drop(
    columns=[
        TARGET_COLUMN,
        "time"
    ]
)

y = df[TARGET_COLUMN]

print("\nFeature Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)


# TRAIN / TEST SPLIT


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE
)

print("\nTrain/Test Split Complete")

print("X_train Shape:", X_train.shape)
print("X_test Shape :", X_test.shape)

print("y_train Shape:", y_train.shape)
print("y_test Shape :", y_test.shape)


# SCALE FEATURES

print("\nScaling numerical features...")

scaler = StandardScaler()

numerical_columns = X_train.select_dtypes(
    include=["number"]
).columns

X_train = X_train.copy()
X_test = X_test.copy()

X_train[numerical_columns] = scaler.fit_transform(
    X_train[numerical_columns]
)

X_test[numerical_columns] = scaler.transform(
    X_test[numerical_columns]
)

joblib.dump(
    scaler,
    SCALER_PATH
)

print(f"Scaler saved to: {SCALER_PATH}")

# TRAIN LINEAR REGRESSION


print("\nTraining Linear Regression Model...")

linear_model = LinearRegression()

linear_model.fit(
    X_train,
    y_train
)

linear_predictions = linear_model.predict(
    X_test
)

print("Linear Regression Training Complete")


# TRAIN RANDOM FOREST


print("\nTraining Random Forest Model...")

rf_model = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    random_state=RANDOM_STATE
)

rf_model.fit(
    X_train,
    y_train
)

rf_predictions = rf_model.predict(
    X_test
)

print("Random Forest Training Complete")


# EVALUATION FUNCTION


def evaluate_model(
    model_name,
    y_true,
    predictions
):

    mae = mean_absolute_error(
        y_true,
        predictions
    )

    mse = mean_squared_error(
        y_true,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_true,
        predictions
    )

    print("\n" + "=" * 50)
    print(model_name)
    print("=" * 50)

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.2f}")

    return mae, rmse, r2


# EVALUATE LINEAR REGRESSION


linear_metrics = evaluate_model(
    "Linear Regression",
    y_test,
    linear_predictions
)


# EVALUATE RANDOM FOREST


rf_metrics = evaluate_model(
    "Random Forest",
    y_test,
    rf_predictions
)


# MODEL COMPARISON TABLE


comparison_df = pd.DataFrame({

    "Model": [
        "Linear Regression",
        "Random Forest"
    ],

    "MAE": [
        linear_metrics[0],
        rf_metrics[0]
    ],

    "RMSE": [
        linear_metrics[1],
        rf_metrics[1]
    ],

    "R2": [
        linear_metrics[2],
        rf_metrics[2]
    ]

})

print("\nModel Comparison")
print(comparison_df)


# SAVE MODEL COMPARISON PLOT


plt.figure(figsize=(8, 6))

plt.bar(
    comparison_df["Model"],
    comparison_df["R2"]
)

plt.ylabel("R² Score")

plt.title("Model Comparison")

plt.tight_layout()

plt.savefig(
    MODEL_COMPARISON_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"\nSaved: {MODEL_COMPARISON_FIGURE}")


# FEATURE IMPORTANCE ANALYSIS


feature_importance = pd.DataFrame({

    "Feature": X_train.columns,

    "Importance": rf_model.feature_importances_

})

feature_importance = feature_importance.sort_values(

    by="Importance",

    ascending=False

)

print("\nTop 10 Most Important Features")

print(
    feature_importance.head(10)
)


# SAVE FEATURE IMPORTANCE PLOT


top_features = feature_importance.head(10)

plt.figure(figsize=(10, 6))

plt.barh(

    top_features["Feature"],

    top_features["Importance"]

)

plt.xlabel("Importance")

plt.title("Top 10 Feature Importance")

plt.gca().invert_yaxis()

plt.tight_layout()

plt.savefig(

    FEATURE_IMPORTANCE_FIGURE,

    dpi=300,

    bbox_inches="tight"

)

plt.close()

print(f"Saved: {FEATURE_IMPORTANCE_FIGURE}")


# RESIDUAL ANALYSIS


linear_residuals = (
    y_test -
    linear_predictions
)

rf_residuals = (
    y_test -
    rf_predictions
)


# SAVE RESIDUAL COMPARISON PLOT


plt.figure(figsize=(8, 6))

plt.hist(
    linear_residuals,
    bins=20,
    alpha=0.5,
    label="Linear Regression"
)

plt.hist(
    rf_residuals,
    bins=20,
    alpha=0.5,
    label="Random Forest"
)

plt.legend()

plt.xlabel("Residual Error")

plt.ylabel("Frequency")

plt.title("Residual Comparison")

plt.tight_layout()

plt.savefig(
    RESIDUAL_COMPARISON_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Saved: {RESIDUAL_COMPARISON_FIGURE}")

# SELECT BEST MODEL


print("\nBest Model Selection")


if rf_metrics[2] > linear_metrics[2]:

    best_model = rf_model
    model_name = "Random Forest"
    best_model_path = RANDOM_FOREST_MODEL_PATH

    best_mae = rf_metrics[0]
    best_rmse = rf_metrics[1]
    best_r2 = rf_metrics[2]

    print("\nSelected Model: Random Forest")

    print(
        f"R² improved from "
        f"{linear_metrics[2]:.2f} "
        f"to "
        f"{rf_metrics[2]:.2f}"
    )

else:

    best_model = linear_model
    model_name = "Linear Regression"
    best_model_path = LINEAR_MODEL_PATH

    best_mae = linear_metrics[0]
    best_rmse = linear_metrics[1]
    best_r2 = linear_metrics[2]

    print("\nSelected Model: Linear Regression")

    print(
        f"R² remained higher at "
        f"{linear_metrics[2]:.2f}"
    )


# SAVE BOTH MODELS


joblib.dump(
    linear_model,
    LINEAR_MODEL_PATH
)

print(
    f"\nLinear Regression model saved to:\n"
    f"{LINEAR_MODEL_PATH}"
)


joblib.dump(
    rf_model,
    RANDOM_FOREST_MODEL_PATH
)

print(
    f"\nRandom Forest model saved to:\n"
    f"{RANDOM_FOREST_MODEL_PATH}"
)


# SAVE BEST MODEL


joblib.dump(
    best_model,
    BEST_MODEL_PATH
)

print(
    f"\nBest model saved to:\n"
    f"{BEST_MODEL_PATH}"
)


# SAVE MODEL METRICS

metrics = {
    "model_name": model_name,
    "r2": round(best_r2, 4),
    "rmse": round(best_rmse, 4),
    "mae": round(best_mae, 4),
    "training_rows": len(df),
    "trained_at": datetime.now(
        ZoneInfo("Europe/London")
    ).strftime(
        "%d %b %Y %H:%M"
    )
}

with open(
    MODEL_METRICS_PATH,
    "w" 
) as file:

    json.dump(
        metrics,
        file,
        indent=4
    )

print(
    f"\nModel metrics saved to:\n"
    f"{MODEL_METRICS_PATH}"
)

# SUMMARY


print("\n" + "=" * 60)
print("MODEL TRAINING SUMMARY")
print("=" * 60)

print(f"Dataset Shape      : {df.shape}")
print(f"Training Samples   : {X_train.shape[0]}")
print(f"Testing Samples    : {X_test.shape[0]}")

print("\nModel Performance")

print(
    f"Linear Regression  -> "
    f"MAE: {linear_metrics[0]:.2f} | "
    f"RMSE: {linear_metrics[1]:.2f} | "
    f"R²: {linear_metrics[2]:.2f}"
)

print(
    f"Random Forest      -> "
    f"MAE: {rf_metrics[0]:.2f} | "
    f"RMSE: {rf_metrics[1]:.2f} | "
    f"R²: {rf_metrics[2]:.2f}"
)

print(f"\nSelected Model     : {model_name}")

print("\nSaved Files")

print(f"Linear Model       : {LINEAR_MODEL_PATH}")
print(f"Random Forest      : {RANDOM_FOREST_MODEL_PATH}")
print(f"Best Model         : {BEST_MODEL_PATH}")
print(f"Scaler             : {SCALER_PATH}")
print(f"Model Metrics      : {MODEL_METRICS_PATH}")

print("\nGenerated Figures")

print(f"Model Comparison   : {MODEL_COMPARISON_FIGURE}")
print(f"Feature Importance : {FEATURE_IMPORTANCE_FIGURE}")
print(f"Residual Plot      : {RESIDUAL_COMPARISON_FIGURE}")

print("\nWeek 8 model comparison completed successfully.")

