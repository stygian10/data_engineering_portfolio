# Weather ETL Pipeline (Week 4)

**Portfolio Project:** Multi-City Weather ETL with Airflow

## Overview

This project implements a **multi-city weather ETL pipeline** using **Python and Apache Airflow**, designed to extract, transform, load, and validate weather data for **London, Menchester, and Edinburgh**.

It demonstrates:

* Real-world ETL design
* Airflow DAG orchestration
* Multi-city data handling
* PostgreSQL integration
* Professional logging and validation

---

## Folder Structure

```
airflow_weather_pipeline/
├── dags/
│   └── weather_etl_dag.py         # Airflow DAG definition
├── tasks/
│   ├── extract_weather.py          # Extract raw data from Open-Meteo API
│   ├── transform_weather.py        # Transform raw CSVs per city
│   ├── load_weather.py             # Load processed CSVs into PostgreSQL
│   └── validate_weather.py         # Validate rows per city and total
├── data/
│   ├── raw/                        # Raw CSVs from API
│   └── processed/                  # Processed CSVs ready to load
├── outputs/                        # Optional outputs / logs
└── README.md
```

---

## Features

1. **Multi-City ETL**: Extracts, transforms, and loads weather data for three cities.
2. **Airflow DAG Orchestration**:

   * `extract → transform → load → validate → end_pipeline`
   * Logs row counts for each city and total rows.
3. **Idempotent Load**: `TRUNCATE TABLE` ensures no duplicate rows on re-runs.
4. **Validation**: Checks total rows and per-city rows; raises errors if missing.
5. **Portfolio Ready**: Professional logging, folder structure, and DAG metadata.

---

## Requirements

* Docker & Docker Compose
* Apache Airflow 3.x
* PostgreSQL (Docker container)
* Python packages: `pandas`, `requests`, `psycopg2`

---

## How to Run

1. Start Docker containers for Airflow and PostgreSQL.
2. Ensure directories `/data/raw` and `/data/processed` exist.
3. Trigger DAG in Airflow UI: `weather_etl_pipeline`.
4. Monitor tasks: extract → transform → load → validate → end_pipeline.
5. Validate PostgreSQL data:

```sql
SELECT city, COUNT(*) FROM weather_data GROUP BY city;
SELECT * FROM weather_data LIMIT 5;
```

---

## Notes

* Extracted raw data saved with timestamp per city.
* Transformation ensures proper column formatting for PostgreSQL.
* Logs printed to Airflow UI for transparency and portfolio demonstration.
* DAG is designed for **daily execution** but can be triggered manually.

---

## Screenshots

* Airflow DAG UI view
* Task logs showing row counts per city
* PostgreSQL table showing multi-city data
