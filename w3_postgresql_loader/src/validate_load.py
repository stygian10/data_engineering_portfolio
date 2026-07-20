from config import TABLE_NAME
from database import get_connection


def validate_load():
    """
    Validate the data loaded into PostgreSQL.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:
        # Total rows
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME};")
        total_rows = cursor.fetchone()[0]

        # Date range
        cursor.execute(
            f"""
            SELECT
                MIN(time),
                MAX(time)
            FROM {TABLE_NAME};
            """
        )

        start_date, end_date = cursor.fetchone()

        # Cities
        cursor.execute(
            f"""
            SELECT DISTINCT city
            FROM {TABLE_NAME}
            ORDER BY city;
            """
        )

        cities = [row[0] for row in cursor.fetchall()]

        print("\n===== DATABASE VALIDATION =====")
        print(f"Table Name     : {TABLE_NAME}")
        print(f"Total Rows     : {total_rows}")
        print(f"Date Range     : {start_date} --> {end_date}")
        print(f"Cities         : {', '.join(cities)}")
        print("Validation     : PASSED")

    except Exception as error:
        print(f"[ERROR] Validation failed: {error}")
        raise

    finally:
        cursor.close()
        connection.close()