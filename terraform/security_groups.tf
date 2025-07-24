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
