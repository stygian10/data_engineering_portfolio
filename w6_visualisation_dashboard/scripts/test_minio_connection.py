import boto3

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
for obj in response.get("Contents", []):
    print(obj["Key"])