# UK Weather Data Cleaner

## Overview
A data cleaning and exploratory analysis project using **Open-Meteo** historical weather data
for London, Manchester, and Edinburgh (2020–2024).

## Key Insights
- Average daily temperature ranges:
  - London: 11.6 °C
  - Manchester: 10.4 °C
  - Edinburgh: 9.7 °C
- 6137 mm total precipitation recorded in the wettest city.
- Dataset: 3 cities × 1827 days (≈5 years).

## Folder Structure
data/
 ├── raw/              - original downloads
 ├── processed/        - cleaned & summarized datasets
figures/               - exported charts
notebooks/             - Jupyter notebooks

## Outputs
- figures/temp_trend_*.png – Daily temperature trends
- figures/precip_bar_YYYY.png – Monthly precipitation comparison
- figures/temp_boxplot_season_city.png – Seasonal temperature spread
- data/processed/city_summary.csv – Aggregated statistics

## How to Run
1. Clone repo & open in VS Code
2. Ensure Python 3.12 + venv installed
3. Open notebook → Run All
4. Results and figures will appear in /figures & /data/processed
