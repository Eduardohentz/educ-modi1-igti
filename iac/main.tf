# HCL - Hashicorp Configuration Language
# Linguagem declarativa

resource "aws_s3_bucket" "datalake" {
  # Parametros de configuracao do recurso escolhido
  bucket = "${var.base_bucket_name}-${var.environment}-${var.account_number}"

  lifecycle {
    ignore_changes = [server_side_encryption_configuration]
  }

  tags = {
    IES   = "IGTI"
    CURSO = "EDC0"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "config" {
  bucket = aws_s3_bucket.datalake.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_object" "codigo_spark" {
  bucket = aws_s3_bucket.datalake.id
  key    = "emr-code/pyspark/job_spark_from_tf.py"
  acl    = "private"
  source = "../job_spark.py"
  etag   = filemd5("../job_spark.py")
}

provider "aws" {
  region = "us-east-1"
}