import psycopg2

from src.config import (
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

    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
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