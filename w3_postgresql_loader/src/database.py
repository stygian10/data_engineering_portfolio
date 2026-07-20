import psycopg2

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        print("[SUCCESS] Connected to PostgreSQL.")

        return connection

    except Exception as error:
        print(f"[ERROR] Failed to connect to PostgreSQL: {error}")
        raise


def close_connection(connection):
    """
    Close the PostgreSQL database connection.
    """

    if connection is not None:
        connection.close()
        print("[INFO] PostgreSQL connection closed.")