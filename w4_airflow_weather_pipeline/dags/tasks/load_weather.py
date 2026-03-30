import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
from datetime import datetime

def load_weather_data():
    """
    Load all processed weather CSVs into PostgreSQL.
    Adds a 'city' column automatically extracted from filename.
    Designed for Airflow PythonOperator.
    """
    processed_dir = Path("/opt/airflow/data/processed")
    processed_files = sorted(processed_dir.glob("weather_processed_*.csv"))

    if not processed_files:
        raise FileNotFoundError("[LOAD] No processed CSV files found to load")

    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow",
        port=5432
    )
    cursor = conn.cursor()

    # FIX: Column renamed from 'relativehumidity_2m' to 'relative_humidity_2m'
    # to match the updated Open-Meteo API parameter and the CSV column produced
    # by extract_weather.py / transform_weather.py.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            city                 TEXT,
            time                 TIMESTAMP,
            temperature_2m       FLOAT,
            relative_humidity_2m FLOAT,
            windspeed_10m        FLOAT
        );
    """)

    # Clear table before load (fresh daily snapshot)
    cursor.execute("TRUNCATE TABLE weather_data;")

    total_rows = 0

    for file in processed_files:
        try:
            df = pd.read_csv(file)

            # Extract city from filename: weather_processed_<City>_YYYYMMDD_HHMMSS.csv
            city_name = file.stem.split("_")[2]
            df["city"] = city_name

            # FIX: Use execute_values for bulk insert — dramatically faster
            # than row-by-row cursor.execute() on 168-row hourly datasets.
            rows = [
                (
                    row["city"],
                    row["time"],
                    row["temperature_2m"],
                    # FIX: corrected column name to match updated extract/transform
                    row["relative_humidity_2m"],
                    row["windspeed_10m"],
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                """
                INSERT INTO weather_data
                    (city, time, temperature_2m, relative_humidity_2m, windspeed_10m)
                VALUES %s
                """,
                rows
            )

            total_rows += len(df)
            print(f"[LOAD {datetime.utcnow()}] Loaded {len(df)} rows for city: {city_name}")

        except Exception as e:
            conn.rollback()
            print(f"[LOAD] Failed to load {file.name}: {e}")
            raise

    conn.commit()
    cursor.close()
    conn.close()

    print(f"[LOAD {datetime.utcnow()}] Total rows loaded: {total_rows}")