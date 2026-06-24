# W8 - MODEL COMPARISON SCRIPT
# Purpose: Compare Linear Regression vs Random Forest Regressor
#
# Outputs:
# - MAE
# - RMSE
# - R² Score
# - Model Comparison Plot
# - Feature Importance Plot
# - Residual Comparison Plot
# ----------------------------------

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
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
    TEST_SIZE
)

# -----------------------------------
# Load Dataset
# -----------------------------------

print("Loading dataset...")

df = pd.read_parquet(DATA_PATH)

print("\nDataset Shape:")
print(df.shape)

print("\nDate Range:")
print(df["date"].min())
print(df["date"].max())

print("\nFirst 5 Rows:")
print(df.head())

# -----------------------------------
# Prepare Features & Target
# -----------------------------------

print("\nPreparing dataset...")

df = df.dropna()

X = df.drop(
    columns=[
        TARGET_COLUMN,
        "date"
    ]
)

y = df[TARGET_COLUMN]

print("\nFeature Shape:")
print(X.shape)

print("\nTarget Shape:")
print(y.shape)

# -----------------------------------
# Train/Test Split
# -----------------------------------

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

# -----------------------------------
# Train Linear Regression
# -----------------------------------

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

# -----------------------------------
# Train Random Forest
# -----------------------------------

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

# -----------------------------------
# Evaluation Function
# -----------------------------------

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

# -----------------------------------
# Evaluate Linear Regression
# -----------------------------------

linear_metrics = evaluate_model(
    "Linear Regression",
    y_test,
    linear_predictions
)

# -----------------------------------
# Evaluate Random Forest
# -----------------------------------

rf_metrics = evaluate_model(
    "Random Forest",
    y_test,
    rf_predictions
)

# -----------------------------------
# Model Comparison Table
# -----------------------------------

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

# -----------------------------------
# Save Model Comparison Plot
# -----------------------------------

plt.figure(figsize=(8, 6))

plt.bar(
    comparison_df["Model"],
    comparison_df["R2"]
)

plt.ylabel("R² Score")
plt.title("Model Comparison")

plt.tight_layout()

plt.savefig(
    "figures/model_comparison.png"
)

plt.close()

print("\nSaved: figures/model_comparison.png")

# -----------------------------------
# Feature Importance Analysis
# -----------------------------------

feature_importance = pd.DataFrame({
    "Feature": X.columns,
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

# -----------------------------------
# Save Feature Importance Plot
# -----------------------------------

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
    "figures/feature_importance.png"
)

plt.close()

print("Saved: figures/feature_importance.png")

# -----------------------------------
# Residual Analysis
# -----------------------------------

linear_residuals = (
    y_test -
    linear_predictions
)

rf_residuals = (
    y_test -
    rf_predictions
)

# -----------------------------------
# Save Residual Comparison Plot
# -----------------------------------

plt.figure(figsize=(8, 6))

plt.hist(
    linear_residuals,
    bins=15,
    alpha=0.5,
    label="Linear Regression"
)

plt.hist(
    rf_residuals,
    bins=15,
    alpha=0.5,
    label="Random Forest"
)

plt.legend()

plt.xlabel("Residual Error")
plt.ylabel("Frequency")

plt.title(
    "Residual Comparison"
)

plt.tight_layout()

plt.savefig(
    "figures/residual_comparison.png"
)

plt.close()

print("Saved: figures/residual_comparison.png")

# -----------------------------------
# Select Best Model
# -----------------------------------

print("\nBest Model Selection")

if rf_metrics[2] > linear_metrics[2]:

    print("\nSelected Model: Random Forest")

    print(
        f"R² improved from "
        f"{linear_metrics[2]:.2f} "
        f"to "
        f"{rf_metrics[2]:.2f}"
    )

else:

    print("\nSelected Model: Linear Regression")

    print(
        f"R² remained higher at "
        f"{linear_metrics[2]:.2f}"
    )

print("\nModel comparison completed successfully.")