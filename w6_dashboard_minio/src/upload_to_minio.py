from pathlib import Path

from minio import S3Error

from .config import (
    MINIO_BUCKET_NAME,
    MINIO_OBJECT_NAME,
    LOCAL_PARQUET_PATH,
)
from .minio_client import get_minio_client


def upload_parquet_dataset():
    """Upload the latest Spark Parquet dataset to MinIO."""

    client = get_minio_client()

    # Create bucket if it doesn't exist
    if not client.bucket_exists(MINIO_BUCKET_NAME):
        client.make_bucket(MINIO_BUCKET_NAME)
        print(f"Created bucket: {MINIO_BUCKET_NAME}")
    else:
        print(f"Bucket already exists: {MINIO_BUCKET_NAME}")

    dataset_path = Path(LOCAL_PARQUET_PATH)

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Parquet dataset not found:\n{dataset_path}"
        )

    # Remove existing dataset
    print(f"\nRemoving existing dataset: {MINIO_OBJECT_NAME}")

    objects = list(
        client.list_objects(
            MINIO_BUCKET_NAME,
            prefix=MINIO_OBJECT_NAME,
            recursive=True,
        )
    )

    for obj in objects:
        client.remove_object(
            MINIO_BUCKET_NAME,
            obj.object_name,
        )

    print(f"Removed {len(objects)} existing file(s).")

    # Find parquet dataset files
    dataset_files = sorted(
        file
        for file in dataset_path.rglob("*")
        if file.is_file() and not file.name.startswith(".")
    )

    if not dataset_files:
        raise FileNotFoundError(
            f"No files found in dataset:\n{dataset_path}"
        )

    # Upload dataset
    print("\nUploading dataset...")

    for file_path in dataset_files:

        object_name = (
            f"{MINIO_OBJECT_NAME}/"
            f"{file_path.relative_to(dataset_path).as_posix()}"
        )

        client.fput_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            file_path=str(file_path),
        )

        print(f"Uploaded: {object_name}")

    print("\n===================================")
    print("Upload completed successfully.")
    print(f"Bucket          : {MINIO_BUCKET_NAME}")
    print(f"Dataset Folder  : {MINIO_OBJECT_NAME}")
    print(f"Files Uploaded  : {len(dataset_files)}")
    print("===================================")


def main():
    try:
        upload_parquet_dataset()

    except FileNotFoundError as error:
        print(f"\nFile Error:\n{error}")

    except S3Error as error:
        print(f"\nMinIO Error:\n{error}")

    except Exception as error:
        print(f"\nUnexpected Error:\n{error}")


if __name__ == "__main__":
    main()