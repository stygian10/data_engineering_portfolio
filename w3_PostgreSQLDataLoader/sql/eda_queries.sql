-- ========================================================
-- EDA Queries for weather_data table
-- Purpose: Basic data exploration and quality checks
-- Updated: 27-Jan-2026 (all queries verified to run)
-- ========================================================

-- 1. Row count by city
-- Purpose: Check data distribution across cities
SELECT
    city,
    COUNT(*) AS row_count
FROM weather_data
GROUP BY city
ORDER BY row_count DESC;

-- 2. Average temperature by season
-- Purpose: Validate seasonal temperature patterns
SELECT
    season,
    ROUND(AVG(temperature_2m_mean)::numeric, 2) AS avg_temperature
FROM weather_data
WHERE temperature_2m_mean IS NOT NULL
GROUP BY season
ORDER BY avg_temperature DESC;

-- 3. Monthly precipitation totals
-- Purpose: Analyze rainfall trends over time
SELECT
    year,
    month,
    ROUND(SUM(precipitation_sum)::numeric, 2) AS total_precipitation
FROM weather_data
WHERE precipitation_sum IS NOT NULL
GROUP BY year, month
ORDER BY year ASC, month ASC;

-- 4. Minimum and maximum temperature
-- Purpose: Check extreme values for anomalies
SELECT
    MIN(temperature_2m_mean) AS min_temperature,
    MAX(temperature_2m_mean) AS max_temperature
FROM weather_data;

-- 5. Missing-value check
-- Purpose: Data quality validation
SELECT
    COUNT(*) FILTER (WHERE temperature_2m_mean IS NULL) AS missing_temperature,
    COUNT(*) FILTER (WHERE precipitation_sum IS NULL) AS missing_precipitation,
    COUNT(*) FILTER (WHERE date IS NULL) AS missing_date,
    COUNT(*) FILTER (WHERE city IS NULL) AS missing_city
FROM weather_data;
