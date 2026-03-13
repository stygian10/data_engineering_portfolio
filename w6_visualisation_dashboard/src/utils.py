# src/utils.py
import pandas as pd
import boto3
from io import BytesIO
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, BUCKET_NAME, PROCESSED_PREFIX

def get_minio_client():
    """Create and return a MinIO (S3) client"""
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY
    )
    return s3

def list_objects(prefix=PROCESSED_PREFIX):
    """List objects in a MinIO bucket under a prefix"""
    s3 = get_minio_client()
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    keys = [obj["Key"] for obj in response.get("Contents", [])]
    return keys

def read_parquet_from_minio(object_key):
    """Download parquet from MinIO and load as pandas DataFrame"""
    try:
        s3 = get_minio_client()
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=object_key)
        df = pd.read_parquet(BytesIO(obj['Body'].read()))
        return df
    except Exception as e:
        print(f"Error loading parquet from MinIO: {e}")
        return None  # Return None if load fails