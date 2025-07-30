output "host_db" {
  description = "Host da instância RDS"
  value       = aws_db_instance.db_ecommerce.address
}

output "url_api" {
  description = "URL da API"
  value       = "https://${aws_api_gateway_rest_api.fake-ecommerce-api.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.dev.stage_name}/${aws_api_gateway_resource.proxy.path_part}"
}

output "arn_api_gateway" {
  description = "ARN da API Gateway"
  value       = aws_api_gateway_rest_api.fake-ecommerce-api.execution_arn
}

resource "terraform_data" "get_db_host" {
  depends_on = [aws_db_instance.db_ecommerce]

  provisioner "local-exec" {
    command = "echo ${aws_db_instance.db_ecommerce.address} > db_host.txt"
  }
}

output "ec2_address" {
  description = "Endereço público da instância EC2"
  value       = aws_instance.api_server.public_dns
}
