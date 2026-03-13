# load_data.py
# Load cleaned weather CSV into PostgreSQL table 'weather_data'
# Matches schema:
#   temperature_2m_mean (float), precipitation_sum (float), date (date),
#   city (string), year (int), month (int), season (string)
# By default this script APPENDS data. Set REPLACE_TABLE = True to replace table contents.

import pandas as pd
from sqlalchemy import text
from db_connect import engine
import sys

# ---------- CONFIG ----------
CSV_PATH = "/Users/gaurav/Documents/Projects/data_engineering_portfolio/weather_etl_pipeline/data/input/uk_weather_clean.csv"  # adjust if needed
TABLE_NAME = "weather_data"
# If True: drop & recreate table contents using pandas.to_sql(if_exists='replace')
# If False: append (default safe mode)
REPLACE_TABLE = False
# pandas.to_sql params
CHUNKSIZE = 1000
METHOD = "multi"  # fast multi-row insert where supported
# ----------------------------

EXPECTED_COLS = [
    "temperature_2m_mean",
    "precipitation_sum",
    "date",
    "city",
    "year",
    "month",
    "season",
]

def read_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # normalize column names: strip, lowercase, replace spaces with underscores
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df

def validate_and_prepare(df: pd.DataFrame) -> pd.DataFrame:
    cols = list(df.columns)
    # Check for expected columns presence
    missing = [c for c in EXPECTED_COLS if c not in cols]
    extra = [c for c in cols if c not in EXPECTED_COLS]
    if missing:
        print(f"ERROR: CSV is missing expected columns: {missing}")
        sys.exit(1)
    if extra:
        print(f"Warning: CSV contains extra columns which will be dropped: {extra}")
        df = df.drop(columns=extra)
    # Convert datatypes
    # date -> pandas datetime.date
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    # numeric conversions (coerce will turn invalids to NaN)
    df["temperature_2m_mean"] = pd.to_numeric(df["temperature_2m_mean"], errors="coerce")
    df["precipitation_sum"] = pd.to_numeric(df["precipitation_sum"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["month"] = pd.to_numeric(df["month"], errors="coerce").astype("Int64")
    # Trim whitespace in string cols
    df["city"] = df["city"].astype(str).str.strip().str.lower()
    df["season"] = df["season"].astype(str).str.strip().str.capitalize()
    # Drop rows with null date or city (essential keys)
    before = len(df)
    df = df.dropna(subset=["date", "city"])
    dropped = before - len(df)
    if dropped:
        print(f"Note: dropped {dropped} rows that lacked date or city after parsing.")
    # Remove duplicate rows within the CSV by (date, city) keeping last
    before = len(df)
    df = df.drop_duplicates(subset=["date", "city"], keep="last").reset_index(drop=True)
    deduped = before - len(df)
    if deduped:
        print(f"Note: removed {deduped} duplicate rows inside the CSV (by date+city).")
    return df

def get_db_count(conn, table: str) -> int:
    res = conn.execute(text(f"SELECT COUNT(*) FROM public.{table};"))
    return res.scalar()

def main():
    print("1) Reading CSV...")
    df = read_csv(CSV_PATH)
    print(f" - raw columns found: {list(df.columns)}")
    print("2) Validating and preparing dataframe...")
    df_prepared = validate_and_prepare(df)
    print(f" - rows to insert after cleaning: {len(df_prepared)}")
    if len(df_prepared) == 0:
        print("No rows to insert. Exiting.")
        return

    # Open a connection and optionally show pre-insert count
    with engine.connect() as conn:
        try:
            before_count = get_db_count(conn, TABLE_NAME)
        except Exception as e:
            print(f"Warning: could not read existing table count (table might not exist yet): {e}")
            before_count = None

    # If REPLACE_TABLE is True, replace the table (drops & recreates)
    if REPLACE_TABLE:
        print("3) REPLACE_TABLE=True → writing data with if_exists='replace' (will replace existing table).")
        # Use pandas to_sql: this will create the table with inferred dtypes if it doesn't exist.
        # Because you already have a create_table.py defining schema, you can also drop manually first.
        df_prepared.to_sql(TABLE_NAME, engine, if_exists="replace", index=False, chunksize=CHUNKSIZE, method=METHOD)
    else:
        print("3) Appending data to existing table (if_exists='append').")
        # Append mode: ensure table exists; if not, to_sql will create it (with potentially different dtypes)
        df_prepared.to_sql(TABLE_NAME, engine, if_exists="append", index=False, chunksize=CHUNKSIZE, method=METHOD)

    # Post-insert summary
    with engine.connect() as conn:
        try:
            after_count = get_db_count(conn, TABLE_NAME)
        except Exception as e:
            print("ERROR: Could not fetch post-insert count:", e)
            after_count = None

    if before_count is None:
        print(f"✅ Insert complete. New total rows in {TABLE_NAME}: {after_count}")
    else:
        inserted = after_count - before_count
        print(f"✅ Insert complete. Rows before: {before_count}, after: {after_count}, inserted: {inserted}")

    print("You can now refresh pgAdmin and inspect the table 'weather_data' (View/Edit Data → All Rows).")

if __name__ == "__main__":
    main()
