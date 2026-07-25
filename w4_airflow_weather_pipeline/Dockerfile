# Base Airflow image
FROM apache/airflow:3.3.0-python3.11

USER root


# Install system dependencies

RUN apt-get update && apt-get install -y \
    build-essential \
    openjdk-17-jdk \
    wget \
    curl \
    unzip \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


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


# PostgreSQL JDBC Driver

RUN mkdir -p /opt/spark/jars && \
    curl -fsSL \
    https://jdbc.postgresql.org/download/postgresql-42.7.7.jar \
    -o /opt/spark/jars/postgresql-42.7.7.jar


# Working directory

WORKDIR /opt/airflow

USER airflow


# Install Python packages

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt


# Verify Java during build

RUN java -version && \
    python -c "import pyspark; print('PySpark:', pyspark.__version__)"


# Default command

CMD ["airflow", "version"]