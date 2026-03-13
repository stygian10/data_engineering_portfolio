import pandas as pd
import psycopg2
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

    # PostgreSQL connection (update credentials if needed)
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow",
        port=5432
    )
    cursor = conn.cursor()

    # Create table if not exists, with city column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            city TEXT,
            time TIMESTAMP,
            temperature_2m FLOAT,
            relativehumidity_2m FLOAT,
            windspeed_10m FLOAT
        );
    """)

    # Clear table before load
    cursor.execute("TRUNCATE TABLE weather_data;")

    total_rows = 0

    for file in processed_files:
        try:
            df = pd.read_csv(file)

            # Extract city from filename: weather_processed_<City>_YYYYMMDD_HHMMSS.csv
            city_name = file.stem.split("_")[2]
            df["city"] = city_name

            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT INTO weather_data (city, time, temperature_2m, relativehumidity_2m, windspeed_10m)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        row["city"],
                        row["time"],
                        row["temperature_2m"],
                        row["relativehumidity_2m"],
                        row["windspeed_10m"]
                    )
                )

            total_rows += len(df)
            print(f"[LOAD {datetime.utcnow()}] Loaded {len(df)} rows for city {city_name}")

        except Exception as e:
            print(f"[LOAD] Failed to load {file.name}: {e}")
            raise

    conn.commit()
    cursor.close()
    conn.close()

    print(f"[LOAD {datetime.utcnow()}] Total rows loaded: {total_rows}")
