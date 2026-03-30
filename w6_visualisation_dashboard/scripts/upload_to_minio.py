import boto3
import os

MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "weather-data-lake"

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

# Create bucket if not exists
try:
    s3.create_bucket(Bucket=BUCKET_NAME)
except:
    pass

local_path = "/opt/airflow/data/parquet"

for file in os.listdir(local_path):
    if file.endswith(".parquet"):
        s3.upload_file(
            os.path.join(local_path, file),
            BUCKET_NAME,
            f"processed/weather/{file}",
        )

print("Uploaded Parquet files to MinIO")