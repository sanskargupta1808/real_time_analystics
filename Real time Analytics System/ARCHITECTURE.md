# System Architecture

## Data Flow

1. **Event Generation**
   - User activities trigger events (page views, clicks, purchases)
   - Events sent to Kafka topic `user-events`

2. **Event Streaming (Kafka)**
   - Producer: Generates continuous stream of user events
   - Topic: 3 partitions for parallel processing
   - Consumer: Reads events and uploads to S3

3. **Raw Storage (S3)**
   - Bucket: `user-events-raw`
   - Format: JSON
   - Partitioning: `raw-events/YYYY/MM/DD/`

4. **ETL Processing (AWS Glue + PySpark)**
   - **Batch Job**: Processes historical data
   - **Streaming Job**: Real-time processing (10-second trigger)
   - Transformations:
     * Data cleaning (null filtering)
     * Timestamp parsing
     * Aggregations (event counts, unique users)
     * Partitioning by date and event type

5. **Processed Storage (S3)**
   - Bucket: `user-events-processed`
   - Format: Parquet (columnar, compressed)
   - Partitioning: `date=YYYY-MM-DD/event_type=XXX/`

6. **Metadata Management (Glue Catalog)**
   - Database: `user_analytics_db`
   - Table: `user_events`
   - Schema versioning and evolution
   - Enables querying with Athena/Redshift Spectrum

## Latency Breakdown

| Stage | Latency |
|-------|---------|
| Kafka Producer → Consumer | < 1 second |
| Consumer → S3 Upload | < 2 seconds |
| Glue Streaming Trigger | 10 seconds |
| PySpark Processing | < 5 seconds |
| **Total End-to-End** | **< 10 seconds** |

## Scalability

- **Kafka**: Horizontal scaling via partitions
- **Glue**: Auto-scaling DPUs (Data Processing Units)
- **S3**: Unlimited storage capacity
- **Processing**: Parallel execution across partitions

## High Availability

- **Kafka**: Replication factor for fault tolerance
- **AWS Glue**: Managed service with automatic retries
- **S3**: 99.999999999% durability
- **Multi-AZ**: Deployment across availability zones
