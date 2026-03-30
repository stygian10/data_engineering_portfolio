# Base Airflow Image
FROM apache/airflow:2.9.3-python3.11

USER root

# Install system dependencies + OpenJDK 17
RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    wget \
    curl \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Correct JAVA_HOME for ARM architecture
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Switch back to airflow user
USER airflow

# Copy Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Optional: mount W5 at runtime via docker-compose (recommended)
# COPY ../w5_spark_weather_etl /opt/airflow/w5