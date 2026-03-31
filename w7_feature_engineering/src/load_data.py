import boto3
import pandas as pd
import os

# ---------------------------
# STEP 1: DOWNLOAD FROM MINIO
# ---------------------------
def download_from_minio():
    MINIO_ENDPOINT = "http://localhost:9000"
    ACCESS_KEY = "minioadmin"
    SECRET_KEY = "minioadmin"
    BUCKET_NAME = "weather-data-lake"

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    os.makedirs("data/raw", exist_ok=True)

    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="processed/weather/")

    parquet_files = []

    for obj in objects.get("Contents", []):
        key = obj["Key"]
        if key.endswith(".parquet"):
            local_path = f"data/raw/{key.split('/')[-1]}"
            s3.download_file(BUCKET_NAME, key, local_path)
            parquet_files.append(local_path)

    print(f"Downloaded {len(parquet_files)} files")
    return parquet_files


# ---------------------------
# STEP 2: LOAD DATA
# ---------------------------
def load_data(parquet_files):
    df_list = [pd.read_parquet(file) for file in parquet_files]
    df = pd.concat(df_list, ignore_index=True)

    print("\nShape:", df.shape)
    print(df.head())

    return df


# ---------------------------
# STEP 3–7: EXPLORATION
# ---------------------------
def explore_data(df):
    print("\nINFO:")
    print(df.info())

    print("\nDESCRIBE:")
    print(df.describe())

    print("\nMISSING VALUES:")
    print(df.isnull().sum().sort_values(ascending=False))

    print("\nDUPLICATES:", df.duplicated().sum())

    # Numeric outliers
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    for col in numeric_cols:
        print(f"\n{col} → Min:", df[col].min(), "Max:", df[col].max())

    # Time check
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by=["city", "date"])
        print("\nTime gaps:")
        print(df.groupby("city")["date"].diff().value_counts())

    return df


# ---------------------------
# STEP 8: SAVE OUTPUT
# ---------------------------
def save_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_parquet("data/processed/w7_exploration.parquet", index=False)
    print("Saved processed file")


# ---------------------------
# MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":
    files = download_from_minio()
    df = load_data(files)
    df = explore_data(df)
    save_data(df)