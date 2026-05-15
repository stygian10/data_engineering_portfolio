# Goal: Evaluate the trained regression model using MAE, RMSE, and R² metrics while generating prediction and residual visualization plots.

# IMPORT LIBRARIES

import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
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
    MODEL_OUTPUT_PATH
)

# LOAD DATA

df = pd.read_parquet(DATA_PATH)

df = df.dropna()

X = df.drop(columns=[TARGET_COLUMN,"date"])

y = df[TARGET_COLUMN]

# TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE
)

# LOAD TRAINED MODEL

model = joblib.load(MODEL_OUTPUT_PATH)

# MAKE PREDICTIONS

predictions = model.predict(X_test)

# EVALUATION METRICS

mae = mean_absolute_error(y_test, predictions)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = mse ** 0.5

r2 = r2_score(y_test, predictions)

print("\nMODEL PERFORMANCE")
print("-" * 40)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.2f}")

# ACTUAL VS PREDICTED PLOT

plt.figure(figsize=(8, 6))

plt.scatter(y_test, predictions)

plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")

plt.title("Actual vs Predicted")

plt.savefig("figures/actual_vs_predicted.png")

print("\nSaved: actual_vs_predicted.png")

# RESIDUAL PLOT

residuals = y_test - predictions

plt.figure(figsize=(8, 6))

plt.hist(residuals, bins=30)

plt.xlabel("Residual Error")
plt.ylabel("Frequency")

plt.title("Residual Distribution")

plt.savefig("figures/residual_distribution.png")

print("Saved: residual_distribution.png")