# load.py
from pathlib import Path

def save_parquet(df, output_folder: str, folder_name: str = None):
    """
    Save Spark DataFrame to Parquet.
    - output_folder: parent folder path
    - folder_name: optional subfolder name for Parquet
    """
    output_path = Path(output_folder)
    if folder_name:
        output_path = output_path / folder_name
    output_path.mkdir(parents=True, exist_ok=True)

    # Save DataFrame as Parquet (distributed, multiple files if large)
    df.write.mode("overwrite").parquet(str(output_path))
    print(f"Saved DataFrame to {output_path}")
    return output_path
