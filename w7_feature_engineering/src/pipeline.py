import pandas as pd
from features import run_feature_pipeline
import os


def load_data():
    df = pd.read_parquet("data/processed/w7_exploration.parquet")
    return df

def save_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_parquet("data/processed/w7_features_final.parquet", index=False)
    print("\nSaved Final ML-ready dataset")


if __name__ == "__main__":
    df = load_data()
    df = run_feature_pipeline(df)
    
    # FINAL DATASET SUMMARY
    
    print("\nFINAL DATASET SUMMARY")
    print("---------------------------")

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    save_data(df)

    save_data(df)