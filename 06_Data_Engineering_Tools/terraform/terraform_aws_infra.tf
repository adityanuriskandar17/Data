# ============================================
# TERRAFORM - INFRASTRUKTUR SEBAGAI KODE
# ============================================
# Membuat infrastruktur data di AWS
# Bahasa Indonesia

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "de-terraform-state"
    key    = "data-infrastructure/terraform.tfstate"
    region = "ap-southeast-1"
  }
}

provider "aws" {
  region = "ap-southeast-1"
}

# --- S3 BUCKET UNTUK DATA LAKE ---
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-prod"
  tags = {
    Name        = "Data Lake"
    Environment = "Production"
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "expire-old-data"
    status = "Enabled"
    filter {
      prefix = "bronze/"
    }
    expiration {
      days = 90
    }
  }

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"
    filter {
      prefix = "silver/"
    }
    transitions {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transitions {
      days          = 90
      storage_class = "GLACIER"
    }
  }
}

# --- IAM ROLE UNTUK GLUE ---
resource "aws_iam_role" "glue_role" {
  name = "glue-etl-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_s3" {
  role       = aws_iam_role.glue_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# --- REDSHIFT CLUSTER ---
resource "aws_redshift_cluster" "dw" {
  cluster_identifier = "data-warehouse-prod"
  database_name      = "dw"
  master_username    = "de_user"
  master_password    = "SecurePassword123!"
  node_type          = "dc2.large"
  cluster_type       = "multi-node"
  number_of_nodes    = 2
  publicly_accessible = false
  skip_final_snapshot = true
}

# --- VPC & SECURITY GROUP ---
resource "aws_security_group" "redshift_sg" {
  name        = "redshift-security-group"
  description = "Security group untuk Redshift"

  ingress {
    from_port   = 5439
    to_port     = 5439
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
