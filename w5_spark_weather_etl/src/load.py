from pathlib import Path

def save_parquet(df, output_folder: str):
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    df.write.mode("overwrite").parquet(str(output_path))

    print(f"✅ Saved Parquet to {output_path}")