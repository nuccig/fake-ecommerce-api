resource "aws_api_gateway_rest_api" "fake-ecommerce-api" {
  name        = "fake-ecommerce-api"
  description = "API com dados simulados de um e-commerce"
}

resource "aws_api_gateway_resource" "fake-ecommerce-api-resource" {
  rest_api_id = aws_api_gateway_rest_api.fake-ecommerce-api.id
  parent_id   = aws_api_gateway_rest_api.fake-ecommerce-api.root_resource_id
  path_part   = "fake-ecommerce"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.fake-ecommerce-api.id
  parent_id   = aws_api_gateway_resource.fake-ecommerce-api-resource.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "fake-ecommerce-api-method" {
  rest_api_id   = aws_api_gateway_rest_api.fake-ecommerce-api.id
  resource_id   = aws_api_gateway_resource.fake-ecommerce-api-resource.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "proxy_method" {
  rest_api_id   = aws_api_gateway_rest_api.fake-ecommerce-api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "ec2_integration" {
  rest_api_id             = aws_api_gateway_rest_api.fake-ecommerce-api.id
  resource_id             = aws_api_gateway_resource.fake-ecommerce-api-resource.id
  http_method             = aws_api_gateway_method.fake-ecommerce-api-method.http_method
  type                    = "HTTP"
  uri                     = "http://${aws_instance.api_server.public_dns}:8000/"
  integration_http_method = "ANY"
}

resource "aws_api_gateway_integration" "ec2_integration_proxy" {
  rest_api_id             = aws_api_gateway_rest_api.fake-ecommerce-api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.proxy_method.http_method
  type                    = "HTTP_PROXY"
  uri                     = "http://${aws_instance.api_server.public_dns}:8000/{proxy+}"
  integration_http_method = "ANY"
}

resource "aws_api_gateway_deployment" "fake-ecommerce-api-deployment" {
  rest_api_id = aws_api_gateway_rest_api.fake-ecommerce-api.id

  depends_on = [
    aws_api_gateway_integration.ec2_integration,
    aws_api_gateway_method.fake-ecommerce-api-method,
    aws_api_gateway_method.proxy_method
  ]
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.fake-ecommerce-api-deployment.id
  rest_api_id   = aws_api_gateway_rest_api.fake-ecommerce-api.id
  stage_name    = "prod"

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      caller         = "$context.identity.caller"
      user           = "$context.identity.user"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      resourcePath   = "$context.resourcePath"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })
  }

  xray_tracing_enabled = false

  depends_on = [aws_api_gateway_account.account]

}
