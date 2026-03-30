# load_data.py
# Load MONTHLY weather summary CSV (W2) into PostgreSQL table
# Target schema:
#   city, year, month, avg_temperature, total_precipitation

import pandas as pd
from sqlalchemy import text
from db_connect import engine
import sys

# ---------- CONFIG ----------
CSV_PATH = "/Users/gaurav/Documents/Projects/data_engineering_portfolio/w2_weather_etl_pipeline/data/output/weather_monthly_summary.csv"
TABLE_NAME = "weather_monthly_summary"

REPLACE_TABLE = False
CHUNKSIZE = 1000
METHOD = "multi"
# ----------------------------

EXPECTED_COLS = [
    "city",
    "year",
    "month",
    "temp_mean",
    "precip_sum",
]

# ----------------------------
# READ CSV
# ----------------------------
def read_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

# ----------------------------
# VALIDATE + CLEAN DATA
# ----------------------------
def validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    print("2) Validating and preparing dataframe...")

    cols = list(df.columns)

    missing = [c for c in EXPECTED_COLS if c not in cols]
    extra = [c for c in cols if c not in EXPECTED_COLS]

    if missing:
        print(f"ERROR: CSV is missing expected columns: {missing}")
        sys.exit(1)

    if extra:
        print(f"Warning: dropping extra columns: {extra}")
        df = df.drop(columns=extra)

    # Convert types
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
    df["temp_mean"] = pd.to_numeric(df["temp_mean"], errors="coerce")
    df["precip_sum"] = pd.to_numeric(df["precip_sum"], errors="coerce")

    # Clean strings
    df["city"] = df["city"].astype(str).str.strip().str.lower()

    # Drop invalid rows
    before = len(df)
    df = df.dropna(subset=["city", "year", "month"])
    dropped = before - len(df)
    if dropped:
        print(f"Note: dropped {dropped} invalid rows")

    # Remove duplicates (monthly uniqueness)
    before = len(df)
    df = df.drop_duplicates(subset=["city", "year", "month"], keep="last")
    deduped = before - len(df)
    if deduped:
        print(f"Note: removed {deduped} duplicate rows")

    # Rename columns for DB clarity
    df = df.rename(columns={
        "temp_mean": "avg_temperature",
        "precip_sum": "total_precipitation"
    })

    return df

# ----------------------------
# DB UTIL
# ----------------------------
def get_db_count(conn, table: str) -> int:
    res = conn.execute(text(f"SELECT COUNT(*) FROM public.{table};"))
    return res.scalar()

# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    print("1) Reading CSV...")
    df = read_csv(CSV_PATH)
    print(f" - columns found: {list(df.columns)}")

    df_prepared = validate_and_prepare(df)
    print(f" - rows ready for insert: {len(df_prepared)}")

    if len(df_prepared) == 0:
        print("No data to insert. Exiting.")
        return

    # Check current row count
    with engine.connect() as conn:
        try:
            before_count = get_db_count(conn, TABLE_NAME)
        except Exception:
            before_count = None

    # Insert into DB
    if REPLACE_TABLE:
        print("3) Replacing table...")
        df_prepared.to_sql(
            TABLE_NAME,
            engine,
            if_exists="replace",
            index=False,
            chunksize=CHUNKSIZE,
            method=METHOD
        )
    else:
        print("3) Appending data...")
        df_prepared.to_sql(
            TABLE_NAME,
            engine,
            if_exists="append",
            index=False,
            chunksize=CHUNKSIZE,
            method=METHOD
        )

    # Post-insert count
    with engine.connect() as conn:
        after_count = get_db_count(conn, TABLE_NAME)

    if before_count is None:
        print(f"✅ Insert complete. Total rows: {after_count}")
    else:
        print(f"✅ Rows before: {before_count}, after: {after_count}, inserted: {after_count - before_count}")

    print("✔ Check pgAdmin → weather_monthly_summary table")

# ----------------------------
if __name__ == "__main__":
    main()