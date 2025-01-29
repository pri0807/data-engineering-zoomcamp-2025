from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, TimestampType, FloatType, StringType
spark = SparkSession.builder.appName("Ingest Data").getOrCreate()
taxi_schema = StructType([
    StructField("VendorID", IntegerType(), True),
    StructField("tpep_pickup_datetime", TimestampType(), True),
    StructField("tpep_dropoff_datetime", TimestampType(), True),
    StructField("passenger_count", IntegerType(), True),
    StructField("trip_distance", FloatType(), True),
    StructField("rate_code_id", IntegerType(), True),
    StructField("store_and_fwd_flag", StringType(), True),
    StructField("PULocationID", IntegerType(), True),
    StructField("DOLocationID", IntegerType(), True),
    StructField("payment_type", StringType(), True),
    StructField("fare_amount", FloatType(), True),
    StructField("extra", FloatType(), True),
    StructField("mta_tax", FloatType(), True),
    StructField("tip_amount", FloatType(), True),
    StructField("tolls_amount", FloatType(), True),
    StructField("improvement_surcharge", FloatType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("congestion_surcharge", FloatType(), True)
])
taxi_full=spark.read.csv("yellow_tripdata_2021-01.csv", header=True, schema=taxi_schema)
db_url = "jdbc:postgresql://localhost:5432/ny_taxi"
db_properties = {
    "user": "root",
    "password": "root",
    "driver": "org.postgresql.Driver"
}
taxi_full.write.jdbc(url=db_url, table="yellow_taxi_data", mode="overwrite", properties=db_properties)

