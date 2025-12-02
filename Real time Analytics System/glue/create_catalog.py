import boto3

glue = boto3.client('glue')

DATABASE_NAME = 'user_analytics_db'
TABLE_NAME = 'user_events'

glue.create_database(
    DatabaseInput={
        'Name': DATABASE_NAME,
        'Description': 'Database for user analytics events'
    }
)

glue.create_table(
    DatabaseName=DATABASE_NAME,
    TableInput={
        'Name': TABLE_NAME,
        'StorageDescriptor': {
            'Columns': [
                {'Name': 'user_id', 'Type': 'string'},
                {'Name': 'event_type', 'Type': 'string'},
                {'Name': 'timestamp', 'Type': 'timestamp'},
                {'Name': 'page', 'Type': 'string'},
                {'Name': 'session_id', 'Type': 'string'},
                {'Name': 'device', 'Type': 'string'},
                {'Name': 'location', 'Type': 'string'},
                {'Name': 'date', 'Type': 'date'},
                {'Name': 'hour', 'Type': 'int'}
            ],
            'Location': 's3://user-events-processed/streaming/',
            'InputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
            }
        },
        'PartitionKeys': [
            {'Name': 'date', 'Type': 'date'},
            {'Name': 'hour', 'Type': 'int'}
        ]
    }
)

print(f"Created database: {DATABASE_NAME}")
print(f"Created table: {TABLE_NAME}")
