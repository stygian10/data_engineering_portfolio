# IMPORT LIBRARIES


import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from config import (
    DATA_PATH,
    TARGET_COLUMN,
    RANDOM_STATE,
    TEST_SIZE,
    MODEL_OUTPUT_PATH
)


# LOAD DATASET


print("Loading dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded successfully.")
print(df.head())


# DATASET OVERVIEW


print("\nDataset Shape:")
print(df.shape)

print("\nMissing Values:")
print(df.isnull().sum())


# REMOVE MISSING VALUES


df = df.dropna()

print("\nDataset Shape After Dropping Nulls:")
print(df.shape)

# DEFINE FEATURES AND TARGET

X = df.drop(columns=[TARGET_COLUMN,"date"])

y = df[TARGET_COLUMN]

print("\nFeature Columns:")
print(X.columns)

# TRAIN TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE
)

print("\nTrain/Test Split Complete")

print(f"X_train Shape: {X_train.shape}")
print(f"X_test Shape: {X_test.shape}")


# TRAIN BASELINE MODEL


print("\nTraining Linear Regression Model...")

model = LinearRegression()

model.fit(X_train, y_train)

print("Model training completed.")


# SAVE MODEL


joblib.dump(model, MODEL_OUTPUT_PATH)

print(f"\nModel saved to: {MODEL_OUTPUT_PATH}")