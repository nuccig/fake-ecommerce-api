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

  depends_on = [null_resource.lambda_dependencies]
}

# Install Python dependencies
resource "null_resource" "lambda_dependencies" {
  triggers = {
    requirements = filemd5("${path.module}/../lambda/requirements.txt")
    source_code  = filemd5("${path.module}/../lambda/update_data.py")
  }

  provisioner "local-exec" {
    working_dir = "${path.module}/../lambda"
    command = "rm -rf package && mkdir -p package && pip install -r requirements.txt -t package/ && cp update_data.py package/"
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

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
      DB_HOST     = file("${path.module}/db_host.txt")
      DB_USER     = var.db_access.username
      DB_PASSWORD = var.db_access.password
      DB_NAME     = var.db_name
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.lambda_logs,
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
  schedule_expression = "rate(1 day)"

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
