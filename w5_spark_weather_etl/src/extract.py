import os
import glob
from pyspark.sql.functions import lit
from pyspark.sql import DataFrame

def extract_data(spark, path_pattern: str) -> DataFrame:
    files = glob.glob(path_pattern)

    if not files:
        raise FileNotFoundError(f"No CSV files found at: {path_pattern}")

    df_list = []

    for file in files:
        # Example filename: weather_processed_London_20260325.csv
        filename = os.path.basename(file)
        city = filename.split("_")[2]  # Adjust if needed

        df = spark.read.csv(file, header=True, inferSchema=True)

        # STANDARDIZE COLUMN NAME (critical fix)
        df = df.withColumnRenamed("relative_humidity_2m", "relativehumidity_2m")

        # Add city column
        df = df.withColumn("city", lit(city))

        df_list.append(df)

    # Combine all files
    combined_df = df_list[0]
    for df in df_list[1:]:
        combined_df = combined_df.unionByName(df)

    return combined_df