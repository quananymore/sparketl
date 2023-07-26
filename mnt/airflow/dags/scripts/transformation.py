import argparse
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, sum, col
from pyspark.sql.types import StructType
from os.path import expanduser, join, abspath
import logging
import datetime
import sys

# set log file name with current date and time
log_file_name = datetime.datetime.now().strftime("/opt/airflow/logs/myapp_%Y-%m-%d_%H-%M-%S.log")

# create logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create file handler with log file name
handler = logging.FileHandler(log_file_name)
handler.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)

# add handler to logger
logger.addHandler(handler)

def main(executionDate):
    # Parse the execution date into year, month and date
    year, month, day = executionDate.split("-")
    warehouse_location = abspath('spark-warehouse')
    logger.info("Execution date %s ",executionDate)

    # Initialize Spark Session
    spark = SparkSession \
        .builder \
        .appName("Daily Result Report") \
        .config("spark.sql.warehouse.dir", warehouse_location) \
        .config("hive.exec.dynamic.partition", "true") \
        .config("hive.exec.dynamic.partition.mode", "nonstrict") \
        .enableHiveSupport() \
        .getOrCreate()

    # load data to spark df
    ordersDF = spark.read.parquet("hdfs://namenode:9000/datalake/orders").drop("year","month","day")
    orderDetailDF = spark.read.parquet("hdfs://namenode:9000/datalake/order_detail").drop("year","month","day")
    productsDF = spark.read.parquet("hdfs://namenode:9000/datalake/products").drop("year","month","day")
    inventoriesDF = spark.read.parquet("hdfs://namenode:9000/datalake/inventories").drop("year","month","day")

    # join dataframes
    preDF = ordersDF \
        .filter(ordersDF["created_at"] <= executionDate) \
        .join(orderDetailDF, ordersDF["id"] == orderDetailDF["order_id"], "inner") \
        .join(productsDF, orderDetailDF["product_id"] == productsDF["id"], "inner") \
        .join(inventoriesDF.select(col("quantity").alias("inv_quantity"), col("id")), productsDF["inventory_id"] == inventoriesDF["id"], "inner")

    # aggregate data
    mapDF = preDF.groupBy("Make","Model","Category","product_id","inv_quantity") \
        .agg(
            sum("quantity").alias("Sales"),
            sum("total").alias("Revenue")
        )

    # prepare result
    resultDF = mapDF \
        .withColumn("leftOver", col("inv_quantity") - col("Sales")) \
        .withColumn("year", lit(year)) \
        .withColumn("month", lit(month)) \
        .withColumn("day", lit(day)) \
        .select("Make", "Model", "Category", "Sales", "Revenue", "leftOver", "year", "month", "day")

    logger.info(resultDF._jdf.showString(100, 20, False))

    logger.info("Number of records: %s",resultDF.count())


    logger.info(spark.read.parquet("hdfs://namenode:9000/datalake/orders").drop("year","month","day")._jdf.showString(100, 20, False))
    logger.info(spark.read.parquet("hdfs://namenode:9000/datalake/orders")._jdf.showString(100, 20, False))

    # write to data warehouse
    resultDF.write \
        .format("hive") \
        .partitionBy("year", "month", "day") \
        .mode("append") \
        .saveAsTable("reports.daily_gross_revenue")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Daily Result Report")
    parser.add_argument("--executionDate", help="Date to filter data by in the format 'YYYY-MM-DD'", required=True)
    args = parser.parse_args()
    # Call the main function
    main(args.executionDate)