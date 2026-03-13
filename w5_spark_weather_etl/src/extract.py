# extract.py
import glob
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, FloatType
from pyspark.sql.functions import lit

def extract_data(spark: SparkSession, path_pattern: str):
    """
    Extract multiple CSV files (matched by glob pattern) into a Spark DataFrame.
    Adds a 'city' column based on the filename for clarity.
    Enforces schema for consistency.
    """

    files = glob.glob(path_pattern)
    if not files:
        raise FileNotFoundError(f"No CSV files found matching: {path_pattern}")

    schema = StructType([
        StructField("time", StringType(), True),
        StructField("temperature_2m", FloatType(), True),
        StructField("relativehumidity_2m", FloatType(), True),
        StructField("windspeed_10m", FloatType(), True),
        StructField("extraction_time", StringType(), True)
    ])

    df_list = []
    for file in files:
        # Infer city name from filename (assumes e.g., "edinburgh_weather.csv")
        city_name = os.path.basename(file).split("_")[0]
        df = spark.read.csv(file, header=True, schema=schema)
        df = df.withColumn("city", lit(city_name))  # add city column
        df_list.append(df)

    # Combine all city DataFrames into one
    combined_df = df_list[0]
    for df in df_list[1:]:
        combined_df = combined_df.unionByName(df)

    return combined_df
