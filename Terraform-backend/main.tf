
 provider "aws" {
  region = "il-central-1"
}

resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "hailyeah-terraform-state"

  #checkov:skip=CKV_AWS_18:Logging isn't needed
  #checkov:skip=CKV2_AWS_62:Notifications aren't needed
  #checkov:skip=CKV2_AWS_61:Lifecycles aren't needed
  #checkov:skip=CKV_AWS_21:Versioning isn't needed
  #checkov:skip=CKV_AWS_145:Encryption isn't needed
  #checkov:skip=CKV_AWS_144:Cross-region replication isn't needed
}

resource "aws_s3_bucket_public_access_block" "access_good" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  block_public_acls   = true
  block_public_policy = true
  restrict_public_buckets = true
  ignore_public_acls=true
}

resource "aws_dynamodb_table" "lock_dynamodb" {
  name = "terraform-lock"
  hash_key = "LockID"
  read_capacity = 5
  write_capacity = 5
 
  attribute {
    name = "LockID"
    type = "S"
  }
  #checkov:skip=CKV_AWS_119:Encryption isn't needed
  #checkov:skip=CKV_AWS_28:Backup isn't needed
  #checkov:skip=CKV2_AWS_16:Auto Scaling isn't needed
}