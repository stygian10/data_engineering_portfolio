# Weather Data Cleaner (Week 2)

**Portfolio Project:** Weather Data Cleaning & Exploration with Python

## Overview
A data cleaning and exploratory analysis project using **Open-Meteo** historical weather data
for London, Manchester, and Edinburgh (2020–2024).

Key objectives:

* Extract weather data from CSV or API sources
* Clean missing and inconsistent values
* Transform data types and column formats
* Perform exploratory data analysis (EDA) for insights
* Save cleaned datasets for downstream pipelines

---

## Folder Structure

```
weather_data_cleaner/
├── data/
│   ├── raw/               # Original raw CSV files
│   └── cleaned/           # Cleaned CSV files ready for ETL
├── notebooks/
│   └── eda_weather.ipynb  # Exploratory data analysis
├── scripts/
│   └── clean_weather.py   # Python script for cleaning data
└── README.md
```

---

## Features

1. **Data Cleaning**:

   * Handle missing values and fill or remove them
   * Standardize column names and data types
   * Remove duplicates or invalid entries

2. **Exploratory Data Analysis (EDA)**:

   * Summary statistics for temperature, humidity, windspeed
   * Visualizations with matplotlib/seaborn (histograms, boxplots, etc.)

3. **Clean Output**:

   * Saves processed datasets to `/data/cleaned`
   * Ready for ETL pipelines in Week 3+

---

## Requirements

* Python 3
* Libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`

---

## How to Run

1. Place raw CSV files in `/data/raw`.
2. Run the cleaning script:

```bash
python scripts/clean_weather.py
```

3. Check cleaned CSVs in `/data/cleaned`.
4. Open `notebooks/eda_weather.ipynb` for visual EDA.

---

## Key Insights
- Average daily temperature ranges:
  - London: 11.6 °C
  - Manchester: 10.4 °C
  - Edinburgh: 9.7 °C
- 6137 mm total precipitation recorded in the wettest city.
- Dataset: 3 cities × 1827 days (≈5 years).

## Notes

* Designed for **portfolio demonstration of data cleaning skills**.
* Modular structure allows easy extension for new weather datasets.
* Cleaned data can feed directly into Week 3 ETL pipelines.

