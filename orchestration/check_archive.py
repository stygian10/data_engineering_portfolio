from datetime import date, datetime, timedelta
import subprocess
import sys

import psycopg2

from orchestration.config import (
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    TABLE_NAME,
    W1_DIR,
    W2_DIR,
    W3_DIR,
)


# =====================================================
# ARCHIVE CONFIGURATION
# =====================================================

ARCHIVE_START_DATE = date(2025, 1, 1)
ARCHIVE_SOURCE = "archive"


# =====================================================
# EXPECTED CITIES
# =====================================================

# These cities are defined by the W1 project configuration.
#
# They are explicitly listed here because archive recovery
# must work even when PostgreSQL contains zero archive rows.
#
# Previously, the archive checker derived the city list
# from existing archive records. When the archive was empty,
# that produced zero cities and therefore zero gaps.

CITIES = [
    "London",
    "Manchester",
    "Edinburgh",
]


# =====================================================
# DATABASE
# =====================================================

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


# =====================================================
# ARCHIVE DATE RANGE
# =====================================================

def get_archive_end_date():
    """
    Return yesterday's date.

    The archive must contain all data from
    ARCHIVE_START_DATE through yesterday.
    """

    return datetime.utcnow().date() - timedelta(days=1)


# =====================================================
# ARCHIVE CHECK
# =====================================================

def find_archive_gaps():
    """
    Find missing archive dates for every configured city.

    Expected archive:

        ARCHIVE_START_DATE -> yesterday

    A date is considered present when at least one
    archive record exists for that city/date.

    Returns
    -------
    list[tuple]
        List of (city, missing_date) pairs.
    """

    archive_end_date = get_archive_end_date()

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # Build the expected city list.
        #
        # This is deliberately independent of PostgreSQL.
        #
        # If there are zero archive records, the expected
        # cities must still exist so missing archive dates
        # can be detected.
        # -------------------------------------------------

        city_values = ", ".join(
            cursor.mogrify(
                "(%s)",
                (city,),
            ).decode()
            for city in CITIES
        )

        cursor.execute(
            f"""
            WITH expected_dates AS (
                SELECT generate_series(
                    %s::date,
                    %s::date,
                    INTERVAL '1 day'
                )::date AS weather_date
            ),

            cities(city) AS (
                VALUES {city_values}
            ),

            expected AS (
                SELECT
                    cities.city,
                    expected_dates.weather_date
                FROM cities
                CROSS JOIN expected_dates
            ),

            actual AS (
                SELECT DISTINCT
                    city,
                    time::date AS weather_date
                FROM {TABLE_NAME}
                WHERE source = %s
                  AND time::date >= %s
                  AND time::date <= %s
            )

            SELECT
                expected.city,
                expected.weather_date

            FROM expected

            LEFT JOIN actual
                ON actual.city = expected.city
               AND actual.weather_date = expected.weather_date

            WHERE actual.weather_date IS NULL

            ORDER BY
                expected.city,
                expected.weather_date;
            """,
            (
                ARCHIVE_START_DATE,
                archive_end_date,
                ARCHIVE_SOURCE,
                ARCHIVE_START_DATE,
                archive_end_date,
            ),
        )

        return cursor.fetchall()

    finally:

        cursor.close()
        connection.close()


# =====================================================
# ARCHIVE STATUS
# =====================================================

def archive_is_complete():
    """
    Determine whether the complete archive exists.
    """

    gaps = find_archive_gaps()

    if gaps:
        return False, gaps

    return True, []


# =====================================================
# RECOVERY COMMANDS
# =====================================================

def run_w1():

    print("\n========== WEEK 1 ==========")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
        ],
        cwd=W1_DIR,
        check=True,
    )


def run_w2():

    print("\n========== WEEK 2 ==========")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
        ],
        cwd=W2_DIR,
        check=True,
    )


def run_w3():

    print("\n========== WEEK 3 ==========")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "src.main",
        ],
        cwd=W3_DIR,
        check=True,
    )


# =====================================================
# PIPELINE DECISION
# =====================================================

def determine_pipeline_branch():

    print("\n========== PIPELINE CHECK ==========\n")

    archive_end_date = get_archive_end_date()

    print(
        f"Expected archive : "
        f"{ARCHIVE_START_DATE} -> {archive_end_date}"
    )

    print(
        f"Archive source   : {ARCHIVE_SOURCE}"
    )

    gaps = find_archive_gaps()

    if gaps:

        print(
            f"\nArchive gaps detected: {len(gaps)} city-days\n"
        )

        current_city = None

        for city, missing_date in gaps:

            if city != current_city:

                print(f"{city}:")

                current_city = city

            print(f"  missing: {missing_date}")

        print(
            "\nArchive status    : INCOMPLETE"
        )

        print(
            "Branch             : run_w1_w2_w3"
        )

        return "run_w1_w2_w3"

    print(
        "\nArchive status    : COMPLETE"
    )

    print(
        "Branch             : skip_recovery"
    )

    return "skip_recovery"


# =====================================================
# AIRFLOW TASKS
# =====================================================

def run_w1_w2_w3():
    """
    Execute Weeks 1–3 archive recovery.
    """

    run_w1()
    run_w2()
    run_w3()


def run_w3_only():
    """
    Execute Week 3 PostgreSQL loading only.

    Kept for compatibility with the existing DAG.
    """

    run_w3()


def skip_recovery():
    """
    Skip archive recovery.
    """

    print("\nRecovery skipped.\n")


# =====================================================
# FORECAST -> ARCHIVE TRANSITION
# =====================================================

def archive_expired_forecasts():
    """
    Reconcile forecast records whose date is before today.

    Rules:
        - Forecast records for today remain forecast.
        - If an expired forecast has a matching archive record,
          remove the forecast duplicate.
        - If an expired forecast has no archive record,
          convert it to archive.

    Returns
    -------
    dict
        Number of rows converted and duplicate forecast rows removed.
    """

    connection = get_connection()
    cursor = connection.cursor()

    try:

        # -------------------------------------------------
        # 1. Convert expired forecast rows that do not
        #    already have an archive counterpart.
        # -------------------------------------------------

        cursor.execute(
            f"""
            UPDATE {TABLE_NAME} AS forecast
            SET source = %s
            WHERE forecast.source = 'forecast'
              AND forecast.time::date < CURRENT_DATE
              AND NOT EXISTS (
                  SELECT 1
                  FROM {TABLE_NAME} AS archive
                  WHERE archive.city = forecast.city
                    AND archive.time = forecast.time
                    AND archive.source = %s
              );
            """,
            (
                ARCHIVE_SOURCE,
                ARCHIVE_SOURCE,
            ),
        )

        converted_rows = cursor.rowcount

        # -------------------------------------------------
        # 2. Remove expired forecast rows where an archive
        #    version already exists.
        # -------------------------------------------------

        cursor.execute(
            f"""
            DELETE FROM {TABLE_NAME} AS forecast
            WHERE forecast.source = 'forecast'
              AND forecast.time::date < CURRENT_DATE
              AND EXISTS (
                  SELECT 1
                  FROM {TABLE_NAME} AS archive
                  WHERE archive.city = forecast.city
                    AND archive.time = forecast.time
                    AND archive.source = %s
              );
            """,
            (ARCHIVE_SOURCE,),
        )

        removed_duplicates = cursor.rowcount

        connection.commit()

        print("\n========== FORECAST TRANSITION ==========")

        print(
            f"Expired forecasts converted to archive : "
            f"{converted_rows}"
        )

        print(
            f"Duplicate expired forecasts removed    : "
            f"{removed_duplicates}"
        )

        print(
            "Today's forecast records               : preserved"
        )

        return {
            "converted": converted_rows,
            "removed_duplicates": removed_duplicates,
        }

    except Exception:

        connection.rollback()
        raise

    finally:

        cursor.close()
        connection.close()