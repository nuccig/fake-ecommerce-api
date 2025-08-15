########################
# Security Groups Lambda
########################

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

  # Permitir saída HTTP
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

########################
# Security Groups RDS
########################

# Obter seu IP atual
data "http" "myip" {
  url = "http://ipv4.icanhazip.com"
}

data "aws_security_group" "airflow_ec2" {
  id = "sg-0455289c93a016f04"
}

resource "aws_security_group" "rds" {
  name_prefix = "ecommerce-rds-"
  vpc_id      = aws_vpc.main.id

  # Acesso da VPC inteira (inclui Lambda nas subnets privadas)
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.main.cidr_block]
  }

  # Meu IP pessoal (para acesso direto ao RDS)
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["${chomp(data.http.myip.response_body)}/32"]
  }

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [data.aws_security_group.airflow_ec2.id]
  }

  #Permite saída para qualquer lugar em todos protocolos
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

########################
# Security Groups EC2
########################

resource "aws_security_group" "ec2" {
  name_prefix = "ecommerce-ec2-"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  #Permite saída para qualquer lugar em todos protocolos
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ec2-api-sg"
  }
}
