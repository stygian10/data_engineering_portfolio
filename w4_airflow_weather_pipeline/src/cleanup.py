from pathlib import Path


RAW_DIR = Path("/opt/airflow/data/raw")
PROCESSED_DIR = Path("/opt/airflow/data/processed")


def cleanup_generated_files():
    print("[CLEANUP] Removing previous raw and processed files...")

    for directory in [RAW_DIR, PROCESSED_DIR]:
        if not directory.exists():
            continue

        for file in directory.iterdir():
            if file.is_file():
                file.unlink()

    print("[CLEANUP] Cleanup complete.")