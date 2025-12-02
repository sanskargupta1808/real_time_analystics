# Getting Started - Visual Guide

## 🎯 What You Have

A complete **Real-time Analytics System** with:
- ✅ Kafka event streaming
- ✅ AWS Glue ETL processing
- ✅ S3 data lake storage
- ✅ < 10 seconds latency
- ✅ Automated pipeline

## 📋 Prerequisites Checklist

- [ ] Python 3 installed
- [ ] AWS CLI installed and configured
- [ ] Kafka installed (optional for local testing)
- [ ] AWS account with appropriate permissions

## 🚀 Three Ways to Start

### Option 1: Full Automated Setup (Recommended)
```bash
cd '/Users/sanskargupta/Desktop/work/ARK_Infosoft/Real time Analytics System'
./setup_all.sh
```

### Option 2: Step-by-Step Setup
```bash
# 1. Install dependencies
pip3 install -r requirements.txt --break-system-packages

# 2. Configure AWS
aws configure

# 3. Create S3 buckets
aws s3 mb s3://user-events-raw
aws s3 mb s3://user-events-processed

# 4. Upload Glue scripts
aws s3 cp glue/etl_job.py s3://user-events-raw/scripts/
aws s3 cp glue/streaming_etl.py s3://user-events-raw/scripts/

# 5. Deploy infrastructure
cd config
terraform init
terraform apply
```

### Option 3: Local Testing Only
```bash
# Install Kafka
brew install kafka

# Start Kafka
./scripts/setup_kafka.sh

# Run producer (Terminal 1)
python3 kafka/producer.py

# Run consumer (Terminal 2)
python3 kafka/consumer.py
```

## 📊 Verify It's Working

### Check 1: Kafka Events
```bash
kafka-console-consumer --topic user-events \
  --bootstrap-server localhost:9092 \
  --from-beginning
```
**Expected**: Stream of JSON events

### Check 2: S3 Raw Data
```bash
aws s3 ls s3://user-events-raw/raw-events/ --recursive
```
**Expected**: JSON files organized by date

### Check 3: S3 Processed Data
```bash
aws s3 ls s3://user-events-processed/streaming/ --recursive
```
**Expected**: Parquet files partitioned by date/hour

### Check 4: Glue Catalog
```bash
aws glue get-table --database-name user_analytics_db \
  --name user_events
```
**Expected**: Table schema definition

### Check 5: Query with Athena
```sql
SELECT event_type, COUNT(*) as count
FROM user_analytics_db.user_events
WHERE date = CURRENT_DATE
GROUP BY event_type;
```
**Expected**: Event counts by type

## 🎨 Architecture Flow

```
┌─────────────┐
│   User App  │
└──────┬──────┘
       │ Events
       ▼
┌─────────────┐
│    Kafka    │ ◄── Producer (kafka/producer.py)
│   Topic     │
└──────┬──────┘
       │ Stream
       ▼
┌─────────────┐
│  Consumer   │ ◄── Consumer (kafka/consumer.py)
└──────┬──────┘
       │ Upload
       ▼
┌─────────────┐
│  S3 Raw     │ ◄── JSON format
│  Storage    │
└──────┬──────┘
       │ Process
       ▼
┌─────────────┐
│ AWS Glue    │ ◄── PySpark ETL (glue/streaming_etl.py)
│ Streaming   │
└──────┬──────┘
       │ Transform
       ▼
┌─────────────┐
│ S3 Processed│ ◄── Parquet format
│  Storage    │
└──────┬──────┘
       │ Catalog
       ▼
┌─────────────┐
│ Glue Catalog│ ◄── Metadata (glue/create_catalog.py)
└──────┬──────┘
       │ Query
       ▼
┌─────────────┐
│  Dashboard  │ ◄── Athena/QuickSight
└─────────────┘
```

## 🔍 Monitoring

```bash
# System health
python3 scripts/monitor.py

# Kafka consumer lag
kafka-consumer-groups --bootstrap-server localhost:9092 \
  --group analytics-consumer --describe

# Glue job status
aws glue get-job-runs --job-name user-events-etl

# CloudWatch logs
aws logs tail /aws-glue/jobs/output --follow
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Kafka connection refused | Start Kafka: `./scripts/setup_kafka.sh` |
| AWS credentials error | Run `aws configure` |
| S3 bucket exists | Change bucket names in terraform.tf |
| Glue job fails | Check CloudWatch logs |
| Import errors | Install: `pip3 install -r requirements.txt` |

## 📈 Performance Tuning

- **Kafka**: Increase partitions for higher throughput
- **Glue**: Adjust DPU count for faster processing
- **S3**: Use S3 Transfer Acceleration for uploads
- **Partitioning**: Optimize based on query patterns

## 🎓 Learning Path

1. **Start**: Run local Kafka producer/consumer
2. **Deploy**: Set up AWS infrastructure
3. **Monitor**: Watch data flow through pipeline
4. **Query**: Run Athena queries on processed data
5. **Optimize**: Tune performance based on metrics

## 📚 Next Steps

- [ ] Create QuickSight dashboard
- [ ] Add data quality checks
- [ ] Implement alerting
- [ ] Set up CI/CD pipeline
- [ ] Add machine learning predictions

## 💡 Pro Tips

- Use `screen` or `tmux` for running multiple processes
- Set up CloudWatch alarms for monitoring
- Enable S3 versioning for data recovery
- Use Glue job bookmarks to avoid reprocessing
- Implement data retention policies

---

**Ready to start?** Run `./setup_all.sh` and follow the prompts!
