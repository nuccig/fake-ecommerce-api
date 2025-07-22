terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.4.0"
    }
  }

  backend "s3" {
    bucket = "nuccig-fake-api-ecommerce"
    key    = "terraform/state"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Environment = "prod"
      Project     = "fake-api"
      ManagedBy   = "Terraform"
      Owner       = "Gustavo Nucci"
    }
  }
}
