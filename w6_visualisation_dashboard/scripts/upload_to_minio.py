import boto3
import os

MINIO_ENDPOINT = "http://minio:9000"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"
BUCKET_NAME = "weather-data-lake"

# CONNECT TO MINIO

s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)


# CREATE BUCKET IF NOT EXISTS

try:
    s3.create_bucket(Bucket=BUCKET_NAME)
except:
    pass


# REMOVE OLD PARQUET FILES

objects = s3.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix="processed/weather/"
)

for obj in objects.get("Contents", []):

    key = obj["Key"]

    if key.endswith(".parquet"):

        s3.delete_object(
            Bucket=BUCKET_NAME,
            Key=key
        )

        print(f"Deleted old file: {key}")


# UPLOAD NEW PARQUET FILES

local_path = "/opt/airflow/data/parquet"

uploaded_count = 0

for file in os.listdir(local_path):

    if file.endswith(".parquet"):

        s3.upload_file(
            os.path.join(local_path, file),
            BUCKET_NAME,
            f"processed/weather/{file}",
        )

        uploaded_count += 1

        print(f"Uploaded: {file}")
        
print(f"\nUploaded {uploaded_count} parquet files to MinIO")