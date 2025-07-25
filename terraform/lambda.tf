data "archive_file" "lambda_update_data" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/package"
  output_path = "${path.module}/../lambda/update_data.zip"

  depends_on = [terraform_data.lambda_dependencies]
}

resource "terraform_data" "lambda_dependencies" {

  triggers_replace = {
    requirements = filemd5("${path.module}/../lambda/requirements.txt")
    source_code  = filemd5("${path.module}/../lambda/update_data.py")
  }

  provisioner "local-exec" {
    working_dir = "${path.module}/../lambda"
    command     = "rm -rf package && mkdir -p package && pip install -r requirements.txt -t package/ && cp update_data.py package/ && cp ../terraform/db_host.txt package/"
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
    aws_iam_role_policy_attachment.lambda_logs,
    aws_iam_role_policy_attachment.lambda_vpc,
    aws_cloudwatch_log_group.lambda_logs
  ]

  tags = {
    Application = "lambda_update_data"
  }
}
