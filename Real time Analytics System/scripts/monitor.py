import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
glue = boto3.client('glue')

def get_glue_job_metrics(job_name):
    response = glue.get_job_runs(JobName=job_name, MaxResults=10)
    
    for run in response['JobRuns']:
        print(f"\nJob Run ID: {run['Id']}")
        print(f"Status: {run['JobRunState']}")
        print(f"Started: {run['StartedOn']}")
        if 'CompletedOn' in run:
            duration = (run['CompletedOn'] - run['StartedOn']).total_seconds()
            print(f"Duration: {duration:.2f} seconds")

def get_s3_metrics(bucket_name):
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/S3',
        MetricName='NumberOfObjects',
        Dimensions=[
            {'Name': 'BucketName', 'Value': bucket_name},
            {'Name': 'StorageType', 'Value': 'AllStorageTypes'}
        ],
        StartTime=datetime.utcnow() - timedelta(hours=1),
        EndTime=datetime.utcnow(),
        Period=3600,
        Statistics=['Average']
    )
    
    if response['Datapoints']:
        print(f"\nS3 Bucket: {bucket_name}")
        print(f"Objects: {response['Datapoints'][0]['Average']:.0f}")

if __name__ == '__main__':
    print("=== Real-time Analytics System Monitoring ===")
    get_glue_job_metrics('user-events-etl')
    get_s3_metrics('user-events-raw')
    get_s3_metrics('user-events-processed')
