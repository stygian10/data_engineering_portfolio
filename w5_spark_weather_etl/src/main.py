from pyspark.sql import SparkSession

from extract import extract_data
from transform import clean_data, aggregate_daily, add_rolling_avg
from load import save_parquet

def main():
    spark = SparkSession.builder.appName("Week5_Weather_ETL").getOrCreate()

    # W4 output (processed CSVs)
    input_path = "/opt/airflow/data/processed/*.csv"
    output_path = "/opt/airflow/data/parquet"

    # ---------------- EXTRACT ----------------
    df = extract_data(spark, input_path)

    # ---------------- TRANSFORM ----------------
    df_clean = clean_data(df)
    df_daily = aggregate_daily(df_clean)
    df_final = add_rolling_avg(df_daily)

    # ---------------- LOAD ----------------
    save_parquet(df_final, output_path)

    spark.stop()
    print("✅ Week 5 ETL completed successfully.")

if __name__ == "__main__":
    main()