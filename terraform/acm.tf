data "aws_acm_certificate" "meu_dominio_cert" {
  domain   = "api.gustavonucci.dev"
  statuses = ["ISSUED"]
}
