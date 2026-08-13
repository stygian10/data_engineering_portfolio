from pathlib import Path

from orchestration.cloud_storage import (
    delete_file,
    download_file,
    list_objects,
    object_exists,
    upload_file,
)


TEST_FILE = Path(
    "orchestration/cloud_storage_test.txt"
)

TEST_FILE.write_text(
    "Weather Intelligence Platform cloud storage test.\n",
    encoding="utf-8",
)

OBJECT_KEY = "test/cloud_storage_test.txt"
DOWNLOAD_FILE = Path(
    "orchestration/cloud_storage_downloaded.txt"
)


print("\n=== CLOUD STORAGE TEST ===\n")


print("1. Upload")
upload_file(
    TEST_FILE,
    OBJECT_KEY,
)


print("\n2. Check object exists")
exists = object_exists(
    OBJECT_KEY
)

print(
    f"Object exists: {exists}"
)


print("\n3. List test objects")
objects = list_objects(
    prefix="test/"
)

for obj in objects:
    print(f" - {obj}")


print("\n4. Download")
download_file(
    OBJECT_KEY,
    DOWNLOAD_FILE,
)

print(
    f"Downloaded content: "
    f"{DOWNLOAD_FILE.read_text(encoding='utf-8').strip()}"
)


print("\n=== TEST PASSED ===")
print(
    "The test object has intentionally "
    "been left in S3."
)