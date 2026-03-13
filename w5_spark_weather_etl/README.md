# Week 5 – Spark Weather ETL

**Project:** Week 5 Spark Re-Write – PySpark ETL pipeline, transformations, Spark SQL, and analysis of weather data per city.

## Overview

This project is part of my **Data Engineering Portfolio 2025–26**. It demonstrates a production-style PySpark ETL pipeline for weather data collected daily across multiple cities.

The pipeline covers:

* Extracting processed CSV data from previous workflow (Week 4)
* Cleaning and transforming data using PySpark
* Aggregating daily statistics and computing rolling averages per city
* Performing Spark SQL analysis (daily, weekly summaries, temperature extremes)
* Saving transformed data as Parquet for downstream analytics
* Optional exploratory visualizations using Matplotlib and Pandas

---

## Tech Stack

* **PySpark** – Core ETL transformations and Spark SQL
* **Pandas** – Combining raw CSVs for initial preprocessing
* **Matplotlib** – Basic visualizations for exploratory analysis
* **Parquet** – Efficient columnar storage for processed data
* **Python 3.x** – Programming language
* **GitHub** – Version control for portfolio management

---

## Project Structure

```
spark_weather_etl/
│
├─ data/
│   ├─ raw/              # Combined raw CSVs from Week 4
│   └─ processed/        # Transformed Parquet outputs
│
├─ src/
│   ├─ extract.py        # Extract CSV data into Spark DataFrame
│   ├─ transform.py      # Data cleaning, aggregation, rolling averages
│   ├─ load.py           # Save processed DataFrames to Parquet
│   └─ main.py           # ETL orchestration
|.  └─ etl_spark
│
├─ notebooks/            # Optional notebooks for analysis/plots
├─ tests/                # Optional Unit tests for ETL modules
└─ README.md
```

---

## ETL Pipeline Steps

1. **Extract** – Load combined Week 4 CSVs into PySpark DataFrame, adding `city` column.
2. **Transform** – Clean data, cast columns to correct types, create `date` column, aggregate daily stats, calculate 3-day rolling averages per city.
3. **Load** – Save processed DataFrame as Parquet.
4. **Analysis (Optional)** – Spark SQL queries for daily & weekly summaries, temperature extremes, and Pandas-based visualizations.

---

## Usage



1. Run the ETL pipeline:

```bash
python main.py
```

2. Processed Parquet files are saved in:

```
data/processed/weather_week5.parquet
```

---

## Future Improvements

* Dockerize PySpark ETL pipeline for containerized execution
* Extend analysis to monthly/seasonal summaries
* Add Airflow orchestration for scheduling
* Integrate cloud storage (S3/MinIO) for raw and processed data


