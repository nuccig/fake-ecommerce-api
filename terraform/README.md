# 🏗️ Infraestrutura AWS Completa
- **Rede Segura**
  - VPC isolada com DNS habilitado
  - Subnets públicas e privadas
  - Internet Gateway para acesso externo
  - Security Groups específicos para cada serviço
  
- **Computação e Aplicação**
  - EC2 t3.micro em subnet pública
  - Docker automatizado com ECR
  - IAM roles para acesso seguro ao ECR
  - User data script para deploy automático
  - Auto-restart de containers
  
- **Banco de Dados**
  - RDS MySQL 8.0 (db.t3.micro)
  - Multi-AZ com subnets em diferentes zonas
  - Backup automático habilitado
  - Acesso público configurado para desenvolvimento
  - Inicialização automática do schema via Terraform
  
- **API Gateway e DNS**
  - API Gateway REST com proxy completo
  - Domínio personalizado (api.gustavonucci.dev)
  - Certificado SSL/TLS via ACM
  - Logs estruturados no CloudWatch
  - Stage de desenvolvimento configurado
  
- **Automação com Lambda**
  - Lambda para atualização diária de dados
  - Trigger automático via CloudWatch Events (3h UTC)
  - Integração com VPC para acesso ao RDS
  - Deploy automático com dependências Python
  - Logs centralizados no CloudWatch