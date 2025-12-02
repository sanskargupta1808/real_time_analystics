provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "raw_events" {
  bucket = "user-events-raw"
}

resource "aws_s3_bucket" "processed_events" {
  bucket = "user-events-processed"
}

resource "aws_glue_catalog_database" "analytics_db" {
  name = "user_analytics_db"
}

resource "aws_glue_job" "etl_job" {
  name     = "user-events-etl"
  role_arn = aws_iam_role.glue_role.arn

  command {
    script_location = "s3://user-events-raw/scripts/etl_job.py"
    python_version  = "3"
  }

  default_arguments = {
    "--JOB_NAME"       = "user-events-etl"
    "--SOURCE_BUCKET"  = aws_s3_bucket.raw_events.id
    "--TARGET_BUCKET"  = aws_s3_bucket.processed_events.id
  }

  glue_version = "4.0"
}

resource "aws_iam_role" "glue_role" {
  name = "glue-etl-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "glue.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "s3_access" {
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ]
      Resource = [
        "${aws_s3_bucket.raw_events.arn}/*",
        "${aws_s3_bucket.processed_events.arn}/*"
      ]
    }]
  })
}
