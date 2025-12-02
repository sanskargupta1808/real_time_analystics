#!/bin/bash

echo "Deploying Real-time Analytics System..."

# Upload Glue scripts to S3
aws s3 cp ../glue/etl_job.py s3://user-events-raw/scripts/
aws s3 cp ../glue/streaming_etl.py s3://user-events-raw/scripts/

# Create Glue Catalog
python3 ../glue/create_catalog.py

# Deploy infrastructure with Terraform
cd ../config
terraform init
terraform apply -auto-approve

echo "Deployment complete!"
