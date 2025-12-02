from kafka import KafkaConsumer
import json
import boto3
from datetime import datetime

consumer = KafkaConsumer(
    'user-events',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='analytics-consumer'
)

s3_client = boto3.client('s3')
BUCKET_NAME = 'user-events-raw'

def upload_to_s3(event):
    date = datetime.utcnow().strftime('%Y/%m/%d')
    key = f"raw-events/{date}/{event['session_id']}_{event['timestamp']}.json"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(event)
    )

if __name__ == '__main__':
    print("Starting consumer...")
    try:
        for message in consumer:
            event = message.value
            print(f"Received: {event['event_type']} - {event['user_id']}")
            upload_to_s3(event)
    except KeyboardInterrupt:
        consumer.close()
        print("\nConsumer stopped")
