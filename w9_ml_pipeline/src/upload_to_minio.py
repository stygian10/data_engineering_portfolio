import boto3

from botocore.exceptions import ClientError

from config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET,
    MINIO_PREFIX,
    PREDICTION_CSV,
    PREDICTION_PARQUET
)


def connect_to_minio():
    """
    Create an S3 client connected to the MinIO server.

    Returns
    -------
    boto3.client
        Configured S3 client.
    """

    print("Connecting to MinIO...")

    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
    )

    print("Connected successfully.")

    return s3


def create_bucket_if_needed(s3):
    """
    Create the bucket if it does not already exist.

    Parameters
    ----------
    s3 : boto3.client
        Connected S3 client.
    """

    try:

        s3.head_bucket(Bucket=MINIO_BUCKET)

        print(f"Bucket already exists: {MINIO_BUCKET}")

    except ClientError:

        print(f"Creating bucket: {MINIO_BUCKET}")

        s3.create_bucket(
            Bucket=MINIO_BUCKET
        )

        print("Bucket created successfully.")


def upload_file(s3, file_path, object_key):
    """
    Upload a single file to MinIO.

    Parameters
    ----------
    s3 : boto3.client
        Connected S3 client.

    file_path : pathlib.Path
        Local file path.

    object_key : str
        Destination object key inside the bucket.
    """

    print(f"\nUploading: {object_key}")

    s3.upload_file(
        Filename=str(file_path),
        Bucket=MINIO_BUCKET,
        Key=object_key
    )

    print("Upload completed.")


def upload_predictions():
    """
    Upload prediction files to MinIO.
    """

    s3 = connect_to_minio()

    create_bucket_if_needed(s3)

    csv_key = MINIO_PREFIX + "weather_predictions.csv"

    parquet_key = MINIO_PREFIX + "weather_predictions.parquet"

    upload_file(
        s3,
        PREDICTION_CSV,
        csv_key
    )

    upload_file(
        s3,
        PREDICTION_PARQUET,
        parquet_key
    )

    print("\nPrediction datasets uploaded successfully.")

    print(f"Bucket: {MINIO_BUCKET}")

    print("Uploaded Objects:")

    print(csv_key)

    print(parquet_key)


if __name__ == "__main__":

    upload_predictions()