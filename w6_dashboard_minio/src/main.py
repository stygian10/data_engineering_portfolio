from minio import S3Error

from .upload_to_minio import (
    upload_parquet_dataset,
)

from .config import (
    MINIO_BUCKET_NAME,
    MINIO_OBJECT_NAME,
)


def main():
    """
    Execute the complete Week 6 pipeline.

    Pipeline
    --------
    1. Upload the latest Spark Parquet dataset to MinIO.
    2. Verify upload completion.
    3. Display pipeline summary.
    """

    print("\n" + "=" * 60)
    print("WEEK 6 PIPELINE STARTED")
    print("=" * 60)

    try:

        upload_parquet_dataset()

        print("\n" + "=" * 60)
        print("WEEK 6 PIPELINE SUMMARY")
        print("=" * 60)

        print(f"Bucket          : {MINIO_BUCKET_NAME}")
        print(f"Dataset Folder  : {MINIO_OBJECT_NAME}")
        print("Status          : SUCCESS")

    except FileNotFoundError as error:

        print("\nFile Error")
        print(error)

        raise

    except S3Error as error:

        print("\nMinIO Error")
        print(error)

        raise

    except Exception as error:

        print("\nUnexpected Error")
        print(error)

        raise

    print("\n" + "=" * 60)
    print("WEEK 6 PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()