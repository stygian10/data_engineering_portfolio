# Weather ETL Pipeline Plan

**Goal:** automate extraction of cleaned weather data → transform into monthly averages → load into new outputs.

## Data Flow
1. **Extract** → read `uk_weather_clean.csv` from Week 1 project.  
2. **Transform** → compute monthly mean temperature & total precipitation per city.  
3. **Load** → save to `data/output/weather_monthly_summary.csv`.  

## Future Extensions
- run automatically via Docker container
- later connect to PostgreSQL (Week 3)
