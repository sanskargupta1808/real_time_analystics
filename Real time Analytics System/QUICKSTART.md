# Quick Start Guide

## For Sentiment Analyzer Training

Run these commands in a separate terminal:

```bash
cd '/Users/sanskargupta/Desktop/work/ARK_Infosoft/Sentiment analyser'
python3 train_svm.py
python3 train_lstm.py
```

## For Real-time Analytics System

### Step 1: Install Dependencies

```bash
cd '/Users/sanskargupta/Desktop/work/ARK_Infosoft/Real time Analytics System'
pip3 install -r requirements.txt --break-system-packages
```

### Step 2: Install Kafka (if not installed)

```bash
brew install kafka
```

### Step 3: Start Kafka

```bash
./scripts/setup_kafka.sh
```

### Step 4: Configure AWS

```bash
aws configure
# Enter your AWS credentials
```

### Step 5: Deploy Infrastructure

```bash
./scripts/deploy.sh
```

### Step 6: Start the Pipeline

**Terminal 1 - Producer:**
```bash
python3 kafka/producer.py
```

**Terminal 2 - Consumer:**
```bash
python3 kafka/consumer.py
```

**Terminal 3 - Monitor:**
```bash
python3 scripts/monitor.py
```

### Step 7: Start Glue ETL Job

```bash
aws glue start-job-run --job-name user-events-etl
```

## Verify Everything Works

1. Check Kafka topic:
```bash
kafka-console-consumer --topic user-events --bootstrap-server localhost:9092 --from-beginning
```

2. Check S3 buckets:
```bash
aws s3 ls s3://user-events-raw/raw-events/
aws s3 ls s3://user-events-processed/streaming/
```

3. Query with Athena:
```sql
SELECT event_type, COUNT(*) as count
FROM user_analytics_db.user_events
GROUP BY event_type;
```

## Troubleshooting

- **Kafka connection refused**: Make sure Kafka is running
- **AWS credentials error**: Run `aws configure`
- **S3 bucket exists**: Change bucket names in terraform.tf
- **Glue job fails**: Check CloudWatch logs

## Success Indicators

✅ Producer sending events
✅ Consumer receiving and uploading to S3
✅ Glue job running successfully
✅ Data appearing in S3 processed bucket
✅ Athena queries returning results
✅ End-to-end latency < 10 seconds
