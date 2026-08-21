FROM apache/airflow:3.3.0-python3.11

USER root

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

RUN JAVA_HOME_PATH=$(dirname $(dirname $(readlink -f $(which java)))) && \
    echo "Detected JAVA_HOME=${JAVA_HOME_PATH}" && \
    ln -s "${JAVA_HOME_PATH}" /usr/lib/jvm/default-java

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH="${JAVA_HOME}/bin:${PATH}"

ENV SPARK_HOME=/home/airflow/.local/lib/python3.11/site-packages/pyspark
ENV PYSPARK_PYTHON=python
ENV PYSPARK_DRIVER_PYTHON=python

RUN mkdir -p /opt/spark/jars && \
    curl -fsSL \
    https://jdbc.postgresql.org/download/postgresql-42.7.7.jar \
    -o /opt/spark/jars/postgresql-42.7.7.jar

WORKDIR /opt/airflow

USER airflow

COPY w4_airflow_weather_pipeline/requirements.txt /tmp/airflow-requirements.txt

RUN pip install --no-cache-dir --user -r /tmp/airflow-requirements.txt

# Copy the same project components currently supplied to Airflow by
# Docker Compose bind mounts.
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root orchestration/ /opt/airflow/orchestration/
COPY --chown=airflow:root w1_weather_data_cleaner/ /opt/airflow/w1/
COPY --chown=airflow:root w2_weather_etl_pipeline/ /opt/airflow/w2/
COPY --chown=airflow:root w3_postgresql_loader/ /opt/airflow/w3/
COPY --chown=airflow:root w4_airflow_weather_pipeline/ /opt/airflow/w4/
COPY --chown=airflow:root w5_spark_weather_etl/ /opt/airflow/w5/
COPY --chown=airflow:root w6_dashboard_minio/ /opt/airflow/w6/
COPY --chown=airflow:root w7_feature_engineering/ /opt/airflow/w7/
COPY --chown=airflow:root w8_weather_prediction_model/ /opt/airflow/w8/
COPY --chown=airflow:root w9_ml_pipeline/ /opt/airflow/w9/

RUN java -version && \
    python -c "import pyspark; print('PySpark:', pyspark.__version__)" && \
    python -c "import psycopg2, boto3, minio, pyarrow, sklearn; print('Core dependencies: OK')"
