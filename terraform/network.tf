#######################
# VPC 
#######################

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ecommerce-vpc"
  }
}

#######################
# IGW 
#######################
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "ecommerce-igw"
  }
}

#######################
# Subnets 
#######################
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "ecommerce-public-subnet-${count.index + 1}"
  }
}

# Para criação em subnets com áreas diferentes e disponíveis
data "aws_availability_zones" "available" {
  state = "available"
}

# Subnets privadas para RDS
resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  tags = {
    Name = "ecommerce-private-subnet-${count.index + 1}"
  }
}

#######################
# Route Table 
#######################
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "ecommerce-public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

#######################
# Subnet pública do RDS 
#######################
resource "aws_db_subnet_group" "main" {
  name       = "ecommerce-db-subnet-group"
  subnet_ids = aws_subnet.public[*].id

  tags = {
    Name = "ecommerce-db-subnet-group"
  }
}
