from database import get_connection
from config import TABLE_NAME


def create_table():
    """Create the weather_data table if it does not exist."""

    connection = get_connection()
    cursor = connection.cursor()

    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        time TIMESTAMP NOT NULL,
        city VARCHAR(50) NOT NULL,
        temperature_2m REAL NOT NULL,
        relative_humidity_2m REAL NOT NULL,
        wind_speed_10m REAL NOT NULL,
        source VARCHAR(20) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (city, time, source)
    );
    """

    try:
        cursor.execute(create_table_query)
        connection.commit()

        print(f"[SUCCESS] Table '{TABLE_NAME}' created successfully.")

    except Exception as error:
        connection.rollback()
        print(f"[ERROR] Failed to create table: {error}")
        raise

    finally:
        cursor.close()
        connection.close()