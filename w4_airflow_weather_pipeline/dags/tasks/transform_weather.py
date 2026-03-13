import pandas as pd
from pathlib import Path
from datetime import datetime

def transform_weather_data():
    """
    Transform all raw weather CSVs in /data/raw and save
    cleaned, processed CSVs to /data/processed.

    Designed for Airflow PythonOperator.
    """
    raw_dir = Path("/opt/airflow/data/raw")
    processed_dir = Path("/opt/airflow/data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_files = sorted(raw_dir.glob("weather_raw_*.csv"))

    if not raw_files:
        raise FileNotFoundError("[TRANSFORM] No raw weather files found to process")

    for raw_file in raw_files:
        try:
            df = pd.read_csv(raw_file)

            # -----------------------------
            # Basic cleaning
            # -----------------------------
            df.columns = [col.lower() for col in df.columns]  # lowercase columns
            df.dropna(inplace=True)  # remove rows with missing values

            # Optional: filter unrealistic values
            df = df[(df['temperature_2m'] > -50) & (df['temperature_2m'] < 60)]
            df = df[(df['relativehumidity_2m'] >= 0) & (df['relativehumidity_2m'] <= 100)]

            # -----------------------------
            # Save processed CSV
            # -----------------------------
            processed_file = processed_dir / raw_file.name.replace("raw", "processed")
            df.to_csv(processed_file, index=False)

            print(f"[TRANSFORM {datetime.utcnow()}] Processed {raw_file.name}")
            print(f"Rows after cleaning: {len(df)} | Saved to: {processed_file}")

        except Exception as e:
            print(f"[TRANSFORM] Failed to process {raw_file.name}: {e}")
            raise
