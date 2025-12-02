import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'SOURCE_BUCKET', 'TARGET_BUCKET'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

source_path = f"s3://{args['SOURCE_BUCKET']}/raw-events/"
target_path = f"s3://{args['TARGET_BUCKET']}/processed-events/"

df = spark.read.json(source_path)

df_cleaned = df \
    .filter(col('user_id').isNotNull()) \
    .filter(col('timestamp').isNotNull()) \
    .withColumn('date', to_date(col('timestamp'))) \
    .withColumn('hour', hour(col('timestamp'))) \
    .withColumn('event_date', date_format(col('timestamp'), 'yyyy-MM-dd'))

df_transformed = df_cleaned \
    .groupBy('event_date', 'event_type', 'device', 'location') \
    .agg(
        count('*').alias('event_count'),
        countDistinct('user_id').alias('unique_users'),
        countDistinct('session_id').alias('unique_sessions')
    )

df_transformed.write \
    .partitionBy('event_date', 'event_type') \
    .mode('overwrite') \
    .parquet(target_path)

job.commit()
