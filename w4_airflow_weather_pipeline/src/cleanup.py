from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
)


def cleanup_generated_files():
    """
    Remove previously generated raw and processed files.
    """

    print("[CLEANUP] Removing previous raw and processed files...")

    for directory in [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
    ]:

        if not directory.exists():
            continue

        for file in directory.iterdir():

            if file.is_file():
                file.unlink()

    print("[CLEANUP] Cleanup complete.")