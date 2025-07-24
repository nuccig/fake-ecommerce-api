terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.4.0"
    }
    http = {
      source  = "hashicorp/http"
      version = "3.5.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.13.1"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "2.7.1"
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

provider "time" {
}

provider "http" {
}

provider "archive" {
}
