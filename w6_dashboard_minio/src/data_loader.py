from pathlib import Path
import shutil

import pandas as pd

from .config import (
    MINIO_BUCKET_NAME,
    MINIO_OBJECT_NAME,
    LOCAL_DOWNLOAD_PATH,
)
from .minio_client import get_minio_client


def load_weather_data():
    """Download the latest dataset from MinIO and return it as a DataFrame."""

    client = get_minio_client()

    download_path = Path(LOCAL_DOWNLOAD_PATH)

    # Remove previous local copy
    if download_path.exists():
        shutil.rmtree(download_path)

    download_path.mkdir(parents=True, exist_ok=True)

    # List dataset files
    objects = list(
        client.list_objects(
            MINIO_BUCKET_NAME,
            prefix=MINIO_OBJECT_NAME,
            recursive=True,
        )
    )

    if not objects:
        raise FileNotFoundError(
            f"No dataset found in MinIO: {MINIO_BUCKET_NAME}/{MINIO_OBJECT_NAME}"
        )

    # Download dataset
    for obj in sorted(objects, key=lambda x: x.object_name):

        relative_path = Path(obj.object_name).relative_to(MINIO_OBJECT_NAME)

        local_file = download_path / relative_path

        local_file.parent.mkdir(parents=True, exist_ok=True)

        client.fget_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=obj.object_name,
            file_path=str(local_file),
        )

    # Read Spark Parquet dataset
    df = pd.read_parquet(download_path)

    return df