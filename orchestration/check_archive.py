from datetime import datetime, timedelta
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
    HISTORICAL_DATASET,
)


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
# DATASET CHECK
# =====================================================

def dataset_exists():
    """
    Check whether the Week 2 processed dataset exists.
    """

    if not HISTORICAL_DATASET.exists():
        return False

    return any(HISTORICAL_DATASET.iterdir())


# =====================================================
# HISTORICAL DATABASE CHECKS
# =====================================================

def historical_rows():
    """
    Return the number of historical records.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM {TABLE_NAME}
        WHERE source = 'historical';
        """
    )

    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count


def latest_historical_date():
    """
    Return the latest historical weather timestamp.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        f"""
        SELECT MAX(time)
        FROM {TABLE_NAME}
        WHERE source = 'historical';
        """
    )

    latest = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return latest


def historical_up_to_date():
    """
    Determine whether historical data is current.
    """

    latest = latest_historical_date()

    if latest is None:
        return False

    expected = datetime.utcnow().date() - timedelta(days=1)

    return latest.date() >= expected


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

    if not dataset_exists():

        print("Historical dataset : MISSING")
        print("Branch             : run_w1_w2_w3")

        return "run_w1_w2_w3"

    print("Historical dataset : FOUND")

    rows = historical_rows()

    print(f"Historical rows    : {rows}")

    if rows == 0:

        print("Database history   : EMPTY")
        print("Branch             : run_w3_only")

        return "run_w3_only"

    latest = latest_historical_date()

    print(f"Latest historical  : {latest}")

    if not historical_up_to_date():

        print("Historical data    : OUTDATED")
        print("Branch             : run_w1_w2_w3")

        return "run_w1_w2_w3"

    print("Historical data    : CURRENT")
    print("Branch             : skip_recovery")

    return "skip_recovery"


# =====================================================
# AIRFLOW TASKS
# =====================================================

def run_w1_w2_w3():
    """
    Execute Weeks 1–3 recovery.
    """

    run_w1()
    run_w2()

    # PostgreSQL table creation is handled by the DAG.
    run_w3()


def run_w3_only():
    """
    Execute Week 3 recovery only.
    """

    # PostgreSQL table creation is handled by the DAG.
    run_w3()


def skip_recovery():
    """
    Skip recovery.
    """

    print("\nRecovery skipped.\n")