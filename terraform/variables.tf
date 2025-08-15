variable "db_access" {
  description = "Valores da instância RDS"
  type = object({
    username = string
    password = string
  })
}

variable "db_name" {
  description = "Nome do banco de dados"
  type        = string
  default     = "ecommerce"
}

variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "aws_account_id" {
  description = "ID da conta da AWS"
  type        = string
  default     = "551715065713"
}

variable "myip" {
  description = "Meu IP pessoal"
  type        = string
  default     = "179.175.250.171"
}
