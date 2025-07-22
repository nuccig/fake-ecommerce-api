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

# Obter seu IP atual
data "http" "myip" {
  url = "http://ipv4.icanhazip.com"
}

# Security Group com seu IP específico
resource "aws_security_group" "rds" {
  name_prefix = "ecommerce-rds-"
  vpc_id      = aws_vpc.main.id

  # Acesso da VPC
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # Seu IP específico para DBeaver
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.myip.response_body)}/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ecommerce-rds-sg"
  }
}

# Usar data source para obter endpoint
data "aws_db_instance" "db_ecommerce" {
  db_instance_identifier = aws_db_instance.db_ecommerce.id
  depends_on             = [aws_db_instance.db_ecommerce]
}

resource "null_resource" "init_db" {
  depends_on = [aws_db_instance.db_ecommerce]

  provisioner "local-exec" {
    command = "python ../data/init_db.py"
    environment = {
      DB_HOST = data.aws_db_instance.db_ecommerce.address
      DB_NAME = var.db_name
      DB_USER = var.db_access.username
      DB_PASS = var.db_access.password
    }
  }

  triggers = {
    db_instance_id = aws_db_instance.db_ecommerce.id
    # timestamp      = timestamp()
  }
}
