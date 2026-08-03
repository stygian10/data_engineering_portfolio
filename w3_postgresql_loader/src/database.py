import psycopg2

from config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
)


def get_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    try:
        connection = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
        )

        print("[SUCCESS] Connected to PostgreSQL.")

        return connection

    except Exception as error:
        print(
            f"[ERROR] Failed to connect to PostgreSQL: {error}"
        )
        raise


def close_connection(connection):
    """
    Close the PostgreSQL database connection.
    """

    if connection is not None:
        connection.close()

        print(
            "[INFO] PostgreSQL connection closed."
        )