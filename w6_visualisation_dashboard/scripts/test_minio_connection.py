import boto3
import pandas as pd
from io import BytesIO

# Create S3 client pointing to MinIO
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
)

bucket_name = "weather-data-lake"

# List objects inside processed/weather/
response = s3.list_objects_v2(
    Bucket=bucket_name,
    Prefix="processed/weather/"
)

print("Objects in processed/weather/:")

keys = []

for obj in response.get("Contents", []):
    print(obj["Key"])
    keys.append(obj["Key"])

# Load parquet file
if keys:
    print("\nLoading parquet file...\n")

    obj = s3.get_object(
        Bucket=bucket_name,
        Key=keys[0]
    )

    df = pd.read_parquet(BytesIO(obj["Body"].read()))

    print(df.head())
    print("\nRows:", len(df))

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    print("\nUnique Cities:")
    print(df["city"].unique())

    print("\nNumber of Cities:", df["city"].nunique())

    print("\nDate Range:")
    print(df["date"].min(), "to", df["date"].max())

    print("\nRows per City:")
    print(df.groupby("city").size())

else:
    print("No files found in bucket")