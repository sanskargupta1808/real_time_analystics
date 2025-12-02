# Real-time Analytics System

A production-grade real-time data pipeline that captures user activity events, processes them with low latency (<10 seconds), and stores them for analytics dashboards.

## Architecture

```
User Events → Kafka → Consumer → S3 (Raw) → AWS Glue ETL → S3 (Processed) → Analytics Dashboard
                                              ↓
                                        Glue Catalog
```

## Components

### 1. Kafka Event Streaming
- **Producer**: Generates and streams user activity events
- **Consumer**: Ingests events and uploads to S3
- **Topic**: `user-events` with 3 partitions

### 2. AWS Glue ETL
- **Batch ETL**: Processes historical data
- **Streaming ETL**: Real-time processing with 10-second latency
- **Transformations**: Cleaning, aggregation, partitioning

### 3. Storage
- **Raw Data**: S3 bucket `user-events-raw`
- **Processed Data**: S3 bucket `user-events-processed`
- **Format**: Parquet with date/hour partitioning

### 4. Metadata Management
- **Glue Catalog**: Schema registry and metadata store
- **Database**: `user_analytics_db`
- **Table**: `user_events`

## Setup

### Prerequisites
```bash
# Install Kafka (macOS)
brew install kafka

# Install Python dependencies
pip3 install -r requirements.txt --break-system-packages

# Configure AWS CLI
aws configure
```

### 1. Start Kafka
```bash
cd scripts
chmod +x setup_kafka.sh
./setup_kafka.sh
```

### 2. Deploy AWS Infrastructure
```bash
cd scripts
chmod +x deploy.sh
./deploy.sh
```

### 3. Start Producer
```bash
cd kafka
python3 producer.py
```

### 4. Start Consumer
```bash
cd kafka
python3 consumer.py
```

### 5. Run Glue ETL Job
```bash
aws glue start-job-run --job-name user-events-etl
```

## Event Schema

```json
{
  "user_id": "user_1234",
  "event_type": "page_view",
  "timestamp": "2025-12-02T10:00:00",
  "page": "/page/1",
  "session_id": "session_123",
  "device": "mobile",
  "location": "US"
}
```

## Performance Metrics

- **Latency**: < 10 seconds end-to-end
- **Throughput**: 1000+ events/second
- **Availability**: 99.9% uptime
- **Data Retention**: 90 days

## Monitoring

```bash
python3 scripts/monitor.py
```

## Project Structure

```
Real time Analytics System/
├── kafka/
│   ├── producer.py          # Event generator
│   └── consumer.py          # Kafka consumer
├── glue/
│   ├── etl_job.py          # Batch ETL
│   ├── streaming_etl.py    # Real-time ETL
│   └── create_catalog.py   # Catalog setup
├── config/
│   └── terraform.tf        # Infrastructure as Code
├── scripts/
│   ├── setup_kafka.sh      # Kafka setup
│   ├── deploy.sh           # Deployment
│   └── monitor.py          # Monitoring
└── README.md
```

## Key Features

✅ Continuous event ingestion from Kafka
✅ Real-time PySpark transformations on AWS Glue
✅ < 10 seconds latency for dashboard updates
✅ Automated pipeline: ingestion → transformation → storage
✅ Partitioned storage for efficient queries
✅ Metadata management with Glue Catalog
✅ Infrastructure as Code with Terraform

## Troubleshooting

### Kafka not starting
```bash
# Check if ports are in use
lsof -i :9092
lsof -i :2181
```

### Glue job failing
```bash
# Check CloudWatch logs
aws logs tail /aws-glue/jobs/output --follow
```

### S3 access denied
```bash
# Verify IAM role permissions
aws iam get-role --role-name glue-etl-role
```
