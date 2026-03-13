from utils import list_objects, read_parquet_from_minio

# List files
keys = list_objects()
print("Objects in bucket:", keys)

# Load dataframe
if keys:
    df = read_parquet_from_minio(keys[0])
    print(df.head())
    print(df.info())
else:
    print("No objects found in bucket")