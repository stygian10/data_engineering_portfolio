import boto3

from botocore.exceptions import ClientError

from .config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_SECURE,
    MINIO_BUCKET_NAME,
    MINIO_PREFIX,
    PREDICTION_CSV,
    PREDICTION_PARQUET,
)


def connect_to_minio():
    """
    Create an S3 client connected to the MinIO server.
    """

    print("Connecting to MinIO...")

    s3 = boto3.client(
        "s3",
        endpoint_url=f"http://{MINIO_ENDPOINT}",
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        use_ssl=MINIO_SECURE,
    )

    print("Connected successfully.")

    return s3


def create_bucket_if_needed(s3):
    """
    Create the bucket if it does not already exist.
    """

    try:

        s3.head_bucket(
            Bucket=MINIO_BUCKET_NAME
        )

        print(
            f"Bucket already exists: {MINIO_BUCKET_NAME}"
        )

    except ClientError:

        print(
            f"Creating bucket: {MINIO_BUCKET_NAME}"
        )

        s3.create_bucket(
            Bucket=MINIO_BUCKET_NAME
        )

        print("Bucket created successfully.")


def upload_file(
    s3,
    file_path,
    object_key,
):
    """
    Upload a single file to MinIO.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found:\n{file_path}"
        )

    print(f"\nUploading: {object_key}")

    s3.upload_file(
        Filename=str(file_path),
        Bucket=MINIO_BUCKET_NAME,
        Key=object_key,
    )

    print("Upload completed.")


def upload_predictions():
    """
    Upload prediction files to MinIO.
    """

    s3 = connect_to_minio()

    create_bucket_if_needed(s3)

    csv_key = (
        MINIO_PREFIX
        + PREDICTION_CSV.name
    )

    parquet_key = (
        MINIO_PREFIX
        + PREDICTION_PARQUET.name
    )

    upload_file(
        s3,
        PREDICTION_CSV,
        csv_key,
    )

    upload_file(
        s3,
        PREDICTION_PARQUET,
        parquet_key,
    )

    print("\nPrediction datasets uploaded successfully.")

    print(f"Bucket: {MINIO_BUCKET_NAME}")

    print("\nUploaded Objects:")

    print(csv_key)

    print(parquet_key)


if __name__ == "__main__":

    upload_predictions()