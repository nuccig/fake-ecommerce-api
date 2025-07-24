#Criando o trigger do CloudWatch para a função Lambda
resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "lambda-update-data-schedule"
  description         = "Trigger lambda daily"
  schedule_expression = "cron(0 3 * * ? *)" # 3 AM UTC daily, meia noite no Brasil
}

#Vinculando o trigger ao Lambda
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.lambda_schedule.name
  target_id = "TriggerLambdaUpdateData"
  arn       = aws_lambda_function.lambda_update_data.arn
}

#Permissão para o CloudWatch invocar a função Lambda
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_update_data.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
}

#Definindo o grupo de logs do CloudWatch para a função Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/lambda_update_data"
  retention_in_days = 14

  tags = {
    Application = "lambda_update_data"
  }
}
