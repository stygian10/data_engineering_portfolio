Configured SQLAlchemy connection to local PostgreSQL instance

#to stand and stop server
 brew services stop postgresql
brew services restart postgresql
 





docker exec -it w4_airflow_weather_pipeline-airflow-apiserver-1 bash
airflow@90e5e1632494:/opt/airflow$ python /opt/airflow/w3/src/main.py