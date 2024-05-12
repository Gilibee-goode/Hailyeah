 terraform {
  backend "s3" {
    encrypt = true
    bucket = "hailyeah-terraform-state"
    dynamodb_table = "terraform-lock"
    key    = "application/terraform.tfstate"
    region = "il-central-1"
  }
}
