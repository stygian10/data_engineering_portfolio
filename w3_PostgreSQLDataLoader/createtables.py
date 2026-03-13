# create_table.py
# This script creates a 'weather_data' table in PostgreSQL with the same columns as your cleaned CSV.

from sqlalchemy import Table, Column, Integer, Float, String, Date, MetaData
from db_connect import engine  # uses your existing connection setup

# Initialize metadata
metadata = MetaData()

# Define the table schema to match the clean_weather.csv structure
weather_data = Table(
    "weather_data",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),  # Auto ID for convenience
    Column("temperature_2m_mean", Float, nullable=True),
    Column("precipitation_sum", Float, nullable=True),
    Column("date", Date, nullable=False),
    Column("city", String(50), nullable=False),
    Column("year", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("season", String(20), nullable=False),
)

# Create the table in PostgreSQL
metadata.create_all(engine)

print("✅ Table 'weather_data' created successfully in PostgreSQL (with 7 matching columns).")
