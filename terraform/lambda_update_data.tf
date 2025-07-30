data "archive_file" "lambda_update_data" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/package-update-data"
  output_path = "${path.module}/../lambda/update_data.zip"

  depends_on = [terraform_data.lambda_dependencies]
}

resource "terraform_data" "lambda_dependencies" {

  triggers_replace = {
    requirements = filemd5("${path.module}/../data/requirements.txt")
    source_code  = filemd5("${path.module}/../data/update_data.py")
  }

  provisioner "local-exec" {
    working_dir = "${path.module}/../lambda"
    command     = "rm -rf package-update-data && mkdir -p package-update-data && pip install -r ../data/requirements.txt -t package-update-data/ && cp ../data/update_data.py package-update-data/ && cp ../terraform/db_host.txt package-update-data/"
  }
}

resource "aws_lambda_function" "lambda_update_data" {
  filename         = data.archive_file.lambda_update_data.output_path #Arquivo usado para executar a função
  description      = "Lambda function to update data in the database"
  function_name    = "lambda_update_data"
  role             = aws_iam_role.lambda_update_data.arn
  handler          = "update_data.lambda_handler"
  source_code_hash = data.archive_file.lambda_update_data.output_base64sha256 # Verifica se o código foi alterado

  runtime = "python3.9"
  timeout = 300

  vpc_config {
    subnet_ids         = aws_subnet.public[*].id
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
      DB_HOST     = data.aws_db_instance.db_ecommerce.address
      DB_USER     = var.db_access.username
      DB_PASSWORD = var.db_access.password
      DB_NAME     = var.db_name
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs_update_data,
    aws_iam_role_policy_attachment.lambda_vpc_update_data,
    aws_cloudwatch_log_group.lambda_logs_update_data
  ]

  tags = {
    Application = "lambda_update_data"
  }
}
