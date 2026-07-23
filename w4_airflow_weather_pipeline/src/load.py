import pandas as pd

from datetime import datetime
from psycopg2.extras import execute_values

from src.config import (
    PROCESSED_DATA_DIR,
    TABLE_NAME,
)

from src.database import get_connection


def load_weather_data():
    """
    Load processed forecast weather data into PostgreSQL.

    Existing forecast records are updated using
    (city, time, source) as the unique key.
    """

    processed_files = sorted(
        PROCESSED_DATA_DIR.glob("weather_processed_*.csv")
    )

    if not processed_files:
        raise FileNotFoundError(
            "[LOAD] No processed weather files found."
        )

    conn = get_connection()
    cursor = conn.cursor()

    total_rows = 0

    try:

        for file in processed_files:

            df = pd.read_csv(file)

            # Extract city from filename
            city = file.stem.split("_")[2]

            df["city"] = city
            df["source"] = "forecast"

            rows = [
                (
                    row["time"],
                    row["city"],
                    row["temperature_2m"],
                    row["relative_humidity_2m"],
                    row["wind_speed_10m"],
                    row["source"],
                )
                for _, row in df.iterrows()
            ]

            execute_values(
                cursor,
                f"""
                INSERT INTO {TABLE_NAME}
                (
                    time,
                    city,
                    temperature_2m,
                    relative_humidity_2m,
                    wind_speed_10m,
                    source
                )
                VALUES %s

                ON CONFLICT (city, time, source)

                DO UPDATE SET

                    temperature_2m = EXCLUDED.temperature_2m,
                    relative_humidity_2m = EXCLUDED.relative_humidity_2m,
                    wind_speed_10m = EXCLUDED.wind_speed_10m;
                """,
                rows,
            )

            total_rows += len(df)

            print(
                f"[LOAD] {city} loaded "
                f"({len(df)} rows)"
            )

        conn.commit()

        print(
            f"[LOAD {datetime.utcnow()}] "
            f"Total rows processed: {total_rows}"
        )

    except Exception as error:

        conn.rollback()

        print(f"[LOAD] Error: {error}")

        raise

    finally:

        cursor.close()
        conn.close()