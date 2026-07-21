import os

import boto3
import pandas as pd

from config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET_NAME,
    MINIO_OBJECT_NAME,
    RAW_DATA_DIR,
    LOCAL_PARQUET_PATH,
)


def download_from_minio():
    """
    Download the latest weather dataset from MinIO.
    """

    print("\nConnecting to MinIO...")

    s3 = boto3.client(
        "s3",
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    print("Connected successfully.")

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    if LOCAL_PARQUET_PATH.exists():
        os.remove(LOCAL_PARQUET_PATH)
        print("Removed old parquet dataset.")

    print(f"\nSearching '{MINIO_OBJECT_NAME}' for parquet files...")

    response = s3.list_objects_v2(
        Bucket=MINIO_BUCKET_NAME,
        Prefix=f"{MINIO_OBJECT_NAME}/",
    )

    parquet_key = None

    for obj in response.get("Contents", []):
        key = obj["Key"]

        if key.endswith(".parquet"):
            parquet_key = key
            break

    if parquet_key is None:
        raise FileNotFoundError(
            f"No parquet file found inside '{MINIO_OBJECT_NAME}'."
        )

    print(f"Found: {parquet_key}")

    print("\nDownloading parquet file...")

    s3.download_file(
        Bucket=MINIO_BUCKET_NAME,
        Key=parquet_key,
        Filename=str(LOCAL_PARQUET_PATH),
    )

    print("Download completed.")

    return LOCAL_PARQUET_PATH


def load_data(parquet_file):
    """
    Load the downloaded parquet dataset.
    """

    weather_df = pd.read_parquet(parquet_file)

    print("\nDataset loaded successfully.")
    print(f"Rows: {len(weather_df)}")
    print(f"Columns: {len(weather_df.columns)}")

    print("\nColumn Names:")
    print(weather_df.columns.tolist())

    return weather_df


if __name__ == "__main__":

    parquet_file = download_from_minio()

    weather_df = load_data(parquet_file)

    print("\nFirst five rows:")
    print(weather_df.head())