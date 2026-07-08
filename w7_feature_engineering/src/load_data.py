import glob
import os

import boto3
import pandas as pd

from config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET_NAME,
    MINIO_PREFIX,
    RAW_DATA_DIR,
)


def download_from_minio():
    """
    Download the latest weather parquet files from MinIO.
    """

    print("\nConnecting to MinIO...")

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    print("Connected successfully.")

    # Create raw directory
    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Remove old raw parquet files
    old_files = glob.glob(
        str(RAW_DATA_DIR / "*.parquet")
    )

    for file in old_files:
        os.remove(file)

    print(f"Removed {len(old_files)} old parquet files.")

    # List objects in MinIO
    response = s3.list_objects_v2(
        Bucket=MINIO_BUCKET_NAME,
        Prefix=MINIO_PREFIX
    )

    parquet_files = []

    for obj in response.get("Contents", []):

        key = obj["Key"]

        if key.endswith(".parquet"):

            local_file = (
                RAW_DATA_DIR
                / key.split("/")[-1]
            )

            s3.download_file(
                MINIO_BUCKET_NAME,
                key,
                str(local_file)
            )

            parquet_files.append(local_file)

    print(f"Downloaded {len(parquet_files)} parquet files.")

    return parquet_files


def load_data(parquet_files):
    """
    Load all downloaded parquet files into one DataFrame.
    """

    df_list = []

    for file in parquet_files:

        df = pd.read_parquet(file)

        df_list.append(df)

    weather_df = pd.concat(
        df_list,
        ignore_index=True
    )

    print("\nDataset loaded successfully.")
    print(f"Rows: {len(weather_df)}")
    print(f"Columns: {len(weather_df.columns)}")

    return weather_df


if __name__ == "__main__":

    files = download_from_minio()

    df = load_data(files)

    print(df.head())