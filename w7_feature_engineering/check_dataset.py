import pandas as pd

df = pd.read_parquet("data/processed/w7_features_final.parquet")

print("\n========== COLUMNS ==========\n")
print(df.columns.tolist())

print("\n========== DATA TYPES ==========\n")
print(df.dtypes)

print("\n========== FIRST 5 ROWS ==========\n")
print(df.head())

print("\n========== SHAPE ==========\n")
print(df.shape)