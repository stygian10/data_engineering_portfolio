# scripts/etl.py
# -----------------------------------------------------------
# WEATHER ETL PIPELINE – auto input/output paths
# Reads from data/input/, writes to data/output/
# -----------------------------------------------------------

from pathlib import Path
import pandas as pd

# ---------- FOLDER SETUP ----------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"

INPUT_CSV = INPUT_DIR / "uk_weather_clean.csv"
OUTPUT_CSV = OUTPUT_DIR / "weather_monthly_summary.csv"
OUTPUT_PARQ = OUTPUT_DIR / "weather_monthly_summary.parquet"

def extract(input_path: Path) -> pd.DataFrame:
    """Read the cleaned daily weather dataset."""
    if not input_path.exists():
        raise FileNotFoundError(f"❌ Input file missing: {input_path}")
    df = pd.read_csv(input_path, parse_dates=["date"])
    print(f"[EXTRACT] rows={len(df):,}, cities={df['city'].nunique()}, "
          f"span={df['date'].min().date()}→{df['date'].max().date()}")
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate monthly mean temperature & total precipitation per city."""
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    monthly = (df.groupby(["city", "year", "month"], as_index=False)
                 .agg(temp_mean=("temperature_2m_mean", "mean"),
                      precip_sum=("precipitation_sum", "sum")))

    monthly["year"] = monthly["year"].astype("int16")
    monthly["month"] = monthly["month"].astype("int8")
    print(f"[TRANSFORM] monthly rows: {len(monthly)}")
    return monthly

def load(df_out: pd.DataFrame) -> None:
    """Save outputs into data/output/ folder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_out.to_csv(OUTPUT_CSV, index=False)
    try:
        df_out.to_parquet(OUTPUT_PARQ, index=False)
    except Exception as e:
        print(f"[LOAD] parquet skipped ({e})")
    print(f"[LOAD] saved CSV → {OUTPUT_CSV.name}")
    if OUTPUT_PARQ.exists():
        print(f"[LOAD] saved PARQUET → {OUTPUT_PARQ.name}")

def main():
    print(f"\n📂 Input → {INPUT_CSV}")
    print(f"📦 Output folder → {OUTPUT_DIR}\n")
    df = extract(INPUT_CSV)
    monthly = transform(df)
    load(monthly)
    print("✅ ETL run complete.\n")

if __name__ == "__main__":
    main()
