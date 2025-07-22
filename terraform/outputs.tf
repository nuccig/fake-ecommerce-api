output "host_db" {
  description = "Host da instância RDS"
  value       = aws_db_instance.db_ecommerce.address
}

resource "null_resource" "get_db_host" {
  depends_on = [aws_db_instance.db_ecommerce]

  provisioner "local-exec" {
    command = "echo ${aws_db_instance.db_ecommerce.address} > db_host.txt"
  }
}
