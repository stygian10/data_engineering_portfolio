import psycopg2

from src.config import (
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

    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def test_connection():
    """
    Test the PostgreSQL connection.
    """

    conn = None

    try:
        conn = get_connection()
        print("[DATABASE] PostgreSQL connection established successfully.")

    except Exception as error:
        print(f"[DATABASE] Connection failed: {error}")
        raise

    finally:
        if conn:
            conn.close()
            print("[DATABASE] Connection closed.")