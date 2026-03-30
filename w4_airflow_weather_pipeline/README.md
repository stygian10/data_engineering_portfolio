[Open-Meteo API]
        │
        ▼
[Extract: extract_weather_data()]
        │
        ▼
[Transform: transform_weather_data()]
        │
        ▼
[Load: load_weather_data() → PostgreSQL]
        │
        ▼
[Validate: validate_weather_data()]
        │
        ▼
[Airflow logs "Pipeline Completed"]

Explanation of your W4 Airflow Weather Pipeline

1	Extract	extract_weather_data() calls Open-Meteo API for London, Manchester, Edinburgh.	Saves raw CSVs in /data/raw.
2	Transform	transform_weather_data() reads raw CSVs, lowercases columns, drops missing/invalid rows, filters unrealistic temp/humidity.	Saves processed CSVs in /data/processed.
3	Load	load_weather_data() inserts cleaned data into PostgreSQL weather_data table.	Makes data queryable by SQL or downstream pipelines.
4	Validate	validate_weather_data() checks row counts per city, ensures table is not empty.	Raises error if validation fails.
5	End pipeline	Logs completion in Airflow.	Confirms ETL success.

docker down/build/up command:

docker compose down -v
docker compose build --no-cache
docker compose up -d

Airflow: 

http://localhost:8080

user & pass: admin