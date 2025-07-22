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
