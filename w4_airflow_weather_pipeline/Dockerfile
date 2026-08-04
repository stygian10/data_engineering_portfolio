# Base Airflow image
FROM apache/airflow:3.3.0-python3.11

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        openjdk-17-jdk \
        wget \
        curl \
        unzip \
        procps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Detect installed Java automatically
RUN JAVA_HOME_PATH=$(dirname $(dirname $(readlink -f $(which java)))) && \
    echo "Detected JAVA_HOME=${JAVA_HOME_PATH}" && \
    ln -s "${JAVA_HOME_PATH}" /usr/lib/jvm/default-java

# Java environment
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

# Spark environment
ENV SPARK_HOME=/home/airflow/.local/lib/python3.11/site-packages/pyspark
ENV PYSPARK_PYTHON=python
ENV PYSPARK_DRIVER_PYTHON=python

# Download PostgreSQL JDBC driver
RUN mkdir -p /opt/spark/jars && \
    curl -fsSL \
    https://jdbc.postgresql.org/download/postgresql-42.7.7.jar \
    -o /opt/spark/jars/postgresql-42.7.7.jar

WORKDIR /opt/airflow

USER airflow

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# Verify Java and PySpark installation
RUN java -version && \
    python -c "import pyspark; print('PySpark:', pyspark.__version__)"

# Copy project files if the Dockerfile is built independently.
# (Your current docker-compose bind mounts will override these.)