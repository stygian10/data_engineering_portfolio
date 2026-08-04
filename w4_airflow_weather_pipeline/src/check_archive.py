from datetime import datetime, timedelta
import subprocess
import psycopg2

from src.config import (
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

print("\n========== PATH CHECK ==========")
print(f"W1_DIR             : {W1_DIR}")
print(f"W2_DIR             : {W2_DIR}")
print(f"W3_DIR             : {W3_DIR}")
print(f"HISTORICAL_DATASET : {HISTORICAL_DATASET}")
print("================================\n")


# DATASET CHECK

def dataset_exists():
    """
    Returns True if the Week 2 processed dataset exists.
    """

    if not HISTORICAL_DATASET.exists():
        return False

    return any(HISTORICAL_DATASET.iterdir())


# DATABASE

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


# DATE CHECK

def historical_up_to_date():
    """
    Check whether historical data is current.
    """

    latest = latest_historical_date()

    if latest is None:
        return False

    expected = datetime.utcnow().date() - timedelta(days=1)

    return latest.date() >= expected


# RECOVERY COMMANDS

def run_week1():

    print("\n========== WEEK 1 ==========")

    subprocess.run(
        ["python", "src/main.py"],
        cwd=W1_DIR,
        check=True,
    )


def run_week2():

    print("\n========== WEEK 2 ==========")

    subprocess.run(
        ["python", "src/main.py"],
        cwd=W2_DIR,
        check=True,
    )


def run_week3():

    print("\n========== WEEK 3 ==========")

    subprocess.run(
        ["python", "src/main.py"],
        cwd=W3_DIR,
        check=True,
    )


# BRANCH DECISION

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


# AIRFLOW TASK FUNCTIONS

def run_w1_w2_w3():
    """
    Execute Weeks 1–3 recovery.
    """

    run_week1()
    run_week2()

    # Table creation is handled by the Airflow DAG.
    run_week3()


def run_w3_only():
    """
    Execute only Week 3 recovery.
    """

    # Table creation is handled by the Airflow DAG.
    run_week3()


def skip_recovery():
    """
    Skip historical recovery.
    """

    print("\nRecovery skipped.\n")