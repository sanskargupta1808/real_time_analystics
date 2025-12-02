from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_user_event():
    events = ['page_view', 'click', 'purchase', 'add_to_cart', 'search']
    return {
        'user_id': f'user_{random.randint(1000, 9999)}',
        'event_type': random.choice(events),
        'timestamp': datetime.utcnow().isoformat(),
        'page': f'/page/{random.randint(1, 50)}',
        'session_id': f'session_{random.randint(100, 999)}',
        'device': random.choice(['mobile', 'desktop', 'tablet']),
        'location': random.choice(['US', 'UK', 'IN', 'CA', 'AU'])
    }

if __name__ == '__main__':
    print("Starting event producer...")
    try:
        while True:
            event = generate_user_event()
            producer.send('user-events', value=event)
            print(f"Sent: {event['event_type']} - {event['user_id']}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        producer.close()
        print("\nProducer stopped")
