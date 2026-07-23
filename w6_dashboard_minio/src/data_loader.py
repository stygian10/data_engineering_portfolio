from pathlib import Path
import shutil

import pandas as pd

from .config import (
    BUCKET_NAME,
    OBJECT_PREFIX,
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
            BUCKET_NAME,
            prefix=OBJECT_PREFIX,
            recursive=True,
        )
    )

    if not objects:
        raise FileNotFoundError(
            f"No dataset found in MinIO: {BUCKET_NAME}/{OBJECT_PREFIX}"
        )

    # Download dataset
    for obj in sorted(objects, key=lambda x: x.object_name):

        relative_path = Path(obj.object_name).relative_to(OBJECT_PREFIX)

        local_file = download_path / relative_path

        local_file.parent.mkdir(parents=True, exist_ok=True)

        client.fget_object(
            bucket_name=BUCKET_NAME,
            object_name=obj.object_name,
            file_path=str(local_file),
        )

    # Read Spark Parquet dataset
    df = pd.read_parquet(download_path)

    return df