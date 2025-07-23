# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_update_data" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Attach CloudWatch logs policy
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_update_data.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/lambda_update_data"
  retention_in_days = 14

  tags = {
    Environment = "production"
    Application = "lambda_update_data"
  }
}

# Package the Lambda function code with dependencies
data "archive_file" "lambda_update_data" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/package"
  output_path = "${path.module}/../lambda/update_data.zip"

  depends_on = [terraform_data.lambda_dependencies]
}

# Install Python dependencies
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

# Lambda function
resource "aws_lambda_function" "lambda_update_data" {
  filename         = data.archive_file.lambda_update_data.output_path
  function_name    = "lambda_update_data"
  role             = aws_iam_role.lambda_update_data.arn
  handler          = "update_data.lambda_handler"
  source_code_hash = data.archive_file.lambda_update_data.output_base64sha256

  runtime = "python3.9"
  timeout = 300

  # Configuração VPC para acessar RDS
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
    Environment = "production"
    Application = "lambda_update_data"
  }
}

# CloudWatch Event Rule para trigger diário
resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "lambda-update-data-schedule"
  description         = "Trigger lambda daily"
  schedule_expression = "cron(0 3 * * ? *)" # 3 AM UTC daily, meia noite no Brasil

  tags = {
    Environment = "production"
  }
}

# CloudWatch Event Target
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  target_id = "TriggerLambdaUpdateData"
  arn       = aws_lambda_function.lambda_update_data.arn
}

# Lambda permission for CloudWatch Events
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_update_data.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
}

# Security Group para Lambda
resource "aws_security_group" "lambda_sg" {
  name_prefix = "lambda-sg-"
  vpc_id      = aws_vpc.main.id

  # Permitir saída para RDS (MySQL) usando CIDR da VPC
  egress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # Permitir saída para internet (HTTPS) - para acessar AWS APIs
  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Permitir saída HTTP (caso necessário)
  egress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "lambda-security-group"
  }
}

# IAM policy para VPC
resource "aws_iam_role_policy_attachment" "lambda_vpc" {
  role       = aws_iam_role.lambda_update_data.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}
