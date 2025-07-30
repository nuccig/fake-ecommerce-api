resource "aws_instance" "api_server" {
  ami                    = "ami-0a7d80731ae1b2435"
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public[0].id
  vpc_security_group_ids = [aws_security_group.ec2.id]

  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.ec2_ecr_profile.name

  key_name = aws_key_pair.ec2_key.key_name

  user_data = <<-EOF
    #!/bin/bash
    sudo apt-get update -y
    sudo apt-get install -y docker.io
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker ubuntu

    docker ps -aq | xargs -r docker stop
    docker ps -aq | xargs -r docker rm

    docker system prune -a --volumes -f

    echo docker --version >> /var/log/user_data_check.log

    sudo apt install unzip -y
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install

    echo aws --version >> /var/log/user_data_check.log

    aws ecr get-login-password --region ${var.aws_region} | sudo docker login --username AWS --password-stdin ${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com

    sudo docker pull ${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/fake-ecommerce-api:latest
    sudo docker run -d --restart unless-stopped -p 8000:8000 --name fake-ecommerce-api \
                -e DB_USER=${var.db_access.username} \
                -e DB_PASSWORD=${var.db_access.password} \
                ${var.aws_account_id}.dkr.ecr.${var.aws_region}.amazonaws.com/fake-ecommerce-api:latest

    sudo docker ps -a >> /var/log/user_data_check.log
    sudo docker logs fake-ecommerce-api >> /var/log/user_data_check.log

    echo "user_data COMPLETO em $(date)" >> /var/log/user_data_check.log
    EOF

  tags = {
    Name = "fake-ecommerce-api-ec2"
  }
}

resource "aws_key_pair" "ec2_key" {
  key_name   = "minha-keypair-ec2"
  public_key = file("~/.ssh/minha-keypair-ec2.pub")
}
