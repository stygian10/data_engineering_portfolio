import psycopg2

def validate_weather_data():
    """
    Validate weather_data table in PostgreSQL.
    Checks total rows and rows per city for multi-city ETL.
    """
    conn = psycopg2.connect(
        host="postgres",
        database="airflow",
        user="airflow",
        password="airflow",
        port=5432
    )

    cursor = conn.cursor()

    # Total row count
    cursor.execute("SELECT COUNT(*) FROM weather_data;")
    total_rows = cursor.fetchone()[0]

    if total_rows == 0:
        raise ValueError("[VALIDATE] Validation failed: weather_data table is empty")
    else:
        print(f"[VALIDATE] Total rows present: {total_rows}")

    # Row count per city
    cursor.execute("SELECT city, COUNT(*) FROM weather_data GROUP BY city;")
    rows_per_city = cursor.fetchall()
    for city, count in rows_per_city:
        print(f"[VALIDATE] City: {city} | Rows: {count}")
        if count == 0:
            raise ValueError(f"[VALIDATE] Validation failed: No data for city {city}")

    print("[VALIDATE] Validation passed for all cities")

    cursor.close()
    conn.close()
