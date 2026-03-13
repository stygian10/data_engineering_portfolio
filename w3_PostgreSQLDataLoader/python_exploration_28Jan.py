# python_exploration_28Jan.py
# This script reconnects to your weather_data table in Postgres
# and prints quick summaries for exploration purposes.
# Safe: does not modify any data.

import pandas as pd
from db_connect import engine  # your existing DB connection

# ---------- Step 1: Fetch sample rows ----------
print("1) Fetching first 100 rows from weather_data...")
df_sample = pd.read_sql("SELECT * FROM weather_data LIMIT 100;", engine)
print(df_sample.head(), "\n")  # show first 5 rows

# ---------- Step 2: Summary statistics ----------
print("2) Numeric summary of your data:")
print(df_sample.describe(), "\n")

# ---------- Step 3: Average temperature per season ----------
print("3) Average temperature per season:")
season_avg = df_sample.groupby('season')['temperature_2m_mean'].mean()
print(season_avg, "\n")

# ---------- Step 4: Row counts per city ----------
print("4) Number of records per city:")
city_counts = df_sample['city'].value_counts()
print(city_counts, "\n")

# ---------- Step 5: Optional checks ----------
print("5) Checking for null values in key columns:")
print(df_sample[['temperature_2m_mean','precipitation_sum','date','city']].isnull().sum(), "\n")

print("✅ Python exploration complete...")