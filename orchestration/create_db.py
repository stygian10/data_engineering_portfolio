import psycopg2

from orchestration.config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    TABLE_NAME,
)


def get_connection():
    """
    Create and return a PostgreSQL connection.
    """

    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def create_table():
    """
    Create the weather_data table if it does not already exist.
    """

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

        print(
            f"PostgreSQL table '{TABLE_NAME}' is ready."
        )

    except Exception as error:

        connection.rollback()

        print(
            f"Failed to create table '{TABLE_NAME}'."
        )

        raise error

    finally:

        cursor.close()

        connection.close()


if __name__ == "__main__":
    create_table()