from src.database import get_connection
from src.config import TABLE_NAME


def validate_weather_data():
    """
    Validate that forecast weather data was loaded
    into the PostgreSQL weather_data table.
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM {TABLE_NAME}
            WHERE source = 'forecast';
            """
        )

        total_rows = cursor.fetchone()[0]

        if total_rows == 0:
            raise ValueError(
                "[VALIDATE] No forecast records found."
            )

        print(
            f"[VALIDATE] Forecast rows: {total_rows}"
        )

        cursor.execute(
            f"""
            SELECT
                city,
                COUNT(*) AS row_count,
                MAX(time) AS latest_forecast
            FROM {TABLE_NAME}
            WHERE source = 'forecast'
            GROUP BY city
            ORDER BY city;
            """
        )

        results = cursor.fetchall()

        if not results:
            raise ValueError(
                "[VALIDATE] No forecast data available."
            )

        for city, count, latest in results:

            print(
                f"[VALIDATE] "
                f"City: {city} | "
                f"Rows: {count} | "
                f"Latest Forecast: {latest}"
            )

            if count == 0:
                raise ValueError(
                    f"[VALIDATE] No forecast data for {city}"
                )

        print(
            "[VALIDATE] Forecast data validation passed."
        )

    finally:

        cursor.close()
        conn.close()