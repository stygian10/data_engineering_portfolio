import pandas as pd

from config import DATA_FILE, TABLE_NAME
from database import get_connection


def load_data():
    """
    Load weather data from the Week 2 processed CSV into PostgreSQL.
    """

    df = pd.read_csv(DATA_FILE)

    connection = get_connection()
    cursor = connection.cursor()

    insert_query = f"""
    INSERT INTO {TABLE_NAME}
    (
        time,
        city,
        temperature_2m,
        relative_humidity_2m,
        wind_speed_10m,
        source
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (city, time, source)
    DO NOTHING;
    """

    rows_inserted = 0

    try:
        for _, row in df.iterrows():
            cursor.execute(
                insert_query,
                (
                    row["time"],
                    row["city"],
                    row["temperature_2m"],
                    row["relative_humidity_2m"],
                    row["wind_speed_10m"],
                    row["source"],
                ),
            )
            rows_inserted += 1

        connection.commit()

        print(f"[SUCCESS] {rows_inserted} rows processed.")

    except Exception as error:
        connection.rollback()
        print(f"[ERROR] Failed to load data: {error}")
        raise

    finally:
        cursor.close()
        connection.close()