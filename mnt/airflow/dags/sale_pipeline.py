from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.email import EmailOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

from datetime import datetime, timedelta
import csv
import requests
import json

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

# Create a new Spark connection
# new_conn = Connection(
#     conn_id='spark_conn',
#     conn_type='spark',
#     host='spark://spark-master',
#     port=7077
# )

# # Add the connection to Airflow's metadata database
# session = settings.Session()
# session.add(new_conn)
# session.commit()
# session.close()


with DAG("sale_pipeline", start_date=datetime(2021, 1 ,1), 
    schedule_interval="@daily", default_args=default_args, catchup=False) as dag:

    saving_sources = BashOperator(
        task_id="saving_sources",
        bash_command="""
            hdfs dfs -mkdir -p /car_sales && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/data/orders.csv /car_sales
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/data/order_detail.csv /car_sales
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/data/products.csv /car_sales
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/data/inventories.csv /car_sales
        """
    )

    creating_results_table = HiveOperator(
        task_id="creating_results_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE DATABASE reports; 
            CREATE EXTERNAL TABLE IF NOT EXISTS reports.daily_gross_revenue(
                Make STRING,
                Model STRING,
                Category STRING,
                Sales INTEGER,
                Revenue INTEGER,
                LeftOver INTEGER
                )
            PARTITIONED BY (year STRING, month STRING, day STRING)
            STORED AS PARQUET;
        """
    )

    ingestion_orders = SparkSubmitOperator(
        task_id="ingestion_orders",
        application="/opt/airflow/dags/scripts/ingestion.py",
        application_args=['--tblName', 'orders', '--executionDate', '2023-07-07'],
        conn_id="spark_conn",
        verbose=False
    )

    ingestion_order_details = SparkSubmitOperator(
        task_id="ingestion_order_details",
        application="/opt/airflow/dags/scripts/ingestion.py",
        application_args=['--tblName', 'order_detail', '--executionDate', '2023-07-07'],
        conn_id="spark_conn",
        verbose=False
    )

    ingestion_products = SparkSubmitOperator(
        task_id="ingestion_products",
        application="/opt/airflow/dags/scripts/ingestion.py",
        application_args=['--tblName', 'products', '--executionDate', '2023-07-07'],
        conn_id="spark_conn",
        verbose=False
    )

    ingestion_inventories = SparkSubmitOperator(
        task_id="ingestion_inventories",
        application="/opt/airflow/dags/scripts/ingestion.py",
        application_args=['--tblName', 'inventories', '--executionDate', '2023-07-07'],
        conn_id="spark_conn",
        verbose=False
    )

    transformation = SparkSubmitOperator(
        task_id="transformation",
        application="/opt/airflow/dags/scripts/transformation.py",
        application_args=['--executionDate', '2023-07-07'],
        conn_id="spark_conn",
        verbose=False
    )

# Set dependencies between tasks
creating_results_table.set_downstream(saving_sources)
saving_sources.set_downstream(ingestion_orders)
saving_sources.set_downstream(ingestion_order_details)
saving_sources.set_downstream(ingestion_products)
saving_sources.set_downstream(ingestion_inventories)

# ingestion_orders.set_downstream(transformation)
# ingestion_order_details.set_downstream(transformation)
# ingestion_products.set_downstream(transformation)
# ingestion_users.set_downstream(transformation)
# ingestion_user_details.set_downstream(transformation)
# ingestion_inventories.set_downstream(transformation)

# saving_sources >> (ingestion_orders,ingestion_order_details,ingestion_products,ingestion_users,ingestion_user_details,ingestion_inventories) >> transformation