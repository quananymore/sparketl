import argparse
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, max
from pyspark.sql.types import StructType
import json

def main(tblName, executionDate):
    # Read the schema from a JSON file

    # with open(f"/opt/airflow/dags/scripts/{tblName}.json") as f:
    #     schema_json = f.read()
    # print(schema_json)
    # schema = StructType.fromJson(json.loads(schema_json))

    # Parse the execution date into year, month and date

    year, month, day = executionDate.split("-")

    spark = SparkSession.builder.appName("Ingestion from Postgres to HDFS").getOrCreate()

    # Check if the table exists in HDFS
    tblLocation = f"hdfs://namenode:9000/datalake/{tblName}"
    
    # fs = spark.sparkContext._gateway.jvm.org.apache.hadoop.fs.FileSystem.get(spark.sparkContext._jsc.hadoopConfiguration())
    # exists = fs.exists(spark.sparkContext._gateway.jvm.org.apache.hadoop.fs.Path(tblLocation))

    # # Determine the query to use based on whether the table exists in HDFS
    # if exists:
    #     print("****************EXISTS********************************")
    #     df = spark.read.schema(schema).parquet(tblLocation)
    #     record_id = df.agg(max("id")).head()[0]
    #     tblQuery = f"(SELECT * FROM `{tblName}` where id > {record_id}) tmp"
    # else:
    #     tblQuery = f"(SELECT * FROM `{tblName}`) tmp"

    # Read data from PostgreSQL
    
    # jdbcDF = spark.read.format("jdbc").option("url", "jdbc:postgresql://0.0.0.0:32769/airflow_db") \
    # .option("driver", "org.postgresql.Driver").option("dbtable", tblQuery) \
    # .option("user", "airflow").option("password", "airflow").load()

    # Manually specify the schema of the Parquet file
    # Read the CSV file into a DataFrame
    # Let Spark know about the header and infer the Schema types!
    jdbcDF = spark.read.csv(f"hdfs://namenode:9000/car_sales/{tblName}.csv",inferSchema=True,header=True)

    # Add year, month, and day columns and write to HDFS
    outputDF = jdbcDF.withColumn("year", lit(year)).withColumn("month", lit(month)).withColumn("day", lit(day))
    outputDF.write.partitionBy("year", "month", "day").mode("append").parquet(tblLocation)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Ingest data from PostgreSQL to HDFS")
    parser.add_argument("--tblName", help="Name of the PostgreSQL table to ingest data from", required=True)
    parser.add_argument("--executionDate", help="Date to filter data by in the format 'YYYY-MM-DD'", required=True)
    args = parser.parse_args()

    # Call the main function
    main(args.tblName, args.executionDate)