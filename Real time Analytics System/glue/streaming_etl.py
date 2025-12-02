import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

schema = StructType([
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("timestamp", StringType()),
    StructField("page", StringType()),
    StructField("session_id", StringType()),
    StructField("device", StringType()),
    StructField("location", StringType())
])

df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "user-events") \
    .load()

df_parsed = df_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*") \
    .withColumn("timestamp", to_timestamp(col("timestamp"))) \
    .withColumn("date", to_date(col("timestamp"))) \
    .withColumn("hour", hour(col("timestamp")))

query = df_parsed.writeStream \
    .format("parquet") \
    .option("path", "s3://user-events-processed/streaming/") \
    .option("checkpointLocation", "s3://user-events-processed/checkpoints/") \
    .partitionBy("date", "hour") \
    .trigger(processingTime='10 seconds') \
    .start()

query.awaitTermination()
