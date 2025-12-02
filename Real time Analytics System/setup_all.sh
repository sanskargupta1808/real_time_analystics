#!/bin/bash

echo "=========================================="
echo "Real-time Analytics System - Full Setup"
echo "=========================================="

# Check prerequisites
echo -e "\n[1/6] Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "Python3 required but not installed."; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "AWS CLI required but not installed."; exit 1; }
echo "✓ Prerequisites OK"

# Install Python dependencies
echo -e "\n[2/6] Installing Python dependencies..."
pip3 install -r requirements.txt --break-system-packages -q
echo "✓ Dependencies installed"

# Check Kafka
echo -e "\n[3/6] Checking Kafka installation..."
if ! command -v kafka-server-start >/dev/null 2>&1; then
    echo "⚠ Kafka not found. Install with: brew install kafka"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ Kafka found"
fi

# AWS Configuration check
echo -e "\n[4/6] Checking AWS configuration..."
if aws sts get-caller-identity >/dev/null 2>&1; then
    echo "✓ AWS credentials configured"
else
    echo "⚠ AWS credentials not configured"
    echo "Run: aws configure"
    exit 1
fi

# Create S3 buckets
echo -e "\n[5/6] Creating S3 buckets..."
aws s3 mb s3://user-events-raw 2>/dev/null && echo "✓ Created user-events-raw" || echo "⚠ Bucket exists or error"
aws s3 mb s3://user-events-processed 2>/dev/null && echo "✓ Created user-events-processed" || echo "⚠ Bucket exists or error"

# Upload Glue scripts
echo -e "\n[6/6] Uploading Glue scripts to S3..."
aws s3 cp glue/etl_job.py s3://user-events-raw/scripts/ && echo "✓ Uploaded etl_job.py"
aws s3 cp glue/streaming_etl.py s3://user-events-raw/scripts/ && echo "✓ Uploaded streaming_etl.py"

echo -e "\n=========================================="
echo "Setup Complete!"
echo "=========================================="
echo -e "\nNext steps:"
echo "1. Start Kafka: ./scripts/setup_kafka.sh"
echo "2. Start Producer: python3 kafka/producer.py"
echo "3. Start Consumer: python3 kafka/consumer.py"
echo "4. Deploy Glue: cd config && terraform init && terraform apply"
echo -e "\nSee QUICKSTART.md for detailed instructions"
