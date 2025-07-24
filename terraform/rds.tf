resource "aws_db_instance" "db_ecommerce" {
  allocated_storage    = 10
  db_name              = var.db_name
  engine               = "mysql"
  engine_version       = "8.0"
  instance_class       = "db.t3.micro"
  username             = var.db_access.username
  password             = var.db_access.password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
  db_subnet_group_name = aws_db_subnet_group.main.name
  publicly_accessible  = true

  vpc_security_group_ids = [aws_security_group.rds.id]

  # Força recriação quando subnet group muda
  lifecycle {
    replace_triggered_by = [
      aws_db_subnet_group.main
    ]
  }
}

# Usar data source para obter endpoint e passar para a lambda
data "aws_db_instance" "db_ecommerce" {
  db_instance_identifier = aws_db_instance.db_ecommerce.id
  depends_on             = [aws_db_instance.db_ecommerce]
}

resource "time_sleep" "wait_for_db" {
  depends_on      = [aws_db_instance.db_ecommerce]
  create_duration = "90s"
}

# Executa um script local para inicializar o banco de dados
resource "terraform_data" "init_db" {
  depends_on = [aws_db_instance.db_ecommerce, time_sleep.wait_for_db]

  provisioner "local-exec" {
    working_dir = "${path.module}/../data"
    command     = "python init_db.py"

    environment = {
      DB_HOST     = data.aws_db_instance.db_ecommerce.address
      DB_NAME     = var.db_name
      DB_USER     = var.db_access.username
      DB_PASSWORD = var.db_access.password
    }
  }

  triggers_replace = {
    db_instance_id = aws_db_instance.db_ecommerce.id
    schema_hash    = filemd5("${path.module}/../data/schema.sql")
    # timestamp      = timestamp()
  }
}
