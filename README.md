# 🛒 Fake E-commerce API

## 📋 Descrição
API REST completa para e-commerce fake com infraestrutura na AWS totalmente automatizada via Terraform e pipeline de CI/CD implementado com GitHub Actions. O projeto demonstra práticas modernas de DevOps incluindo containerização, infraestrutura como código e deploy automatizado.

**🎯 Objetivo do Projeto**: Fornecer uma API com dados fictícios dinâmicos para estudos e desenvolvimento, com atualização automática diária dos dados via Lambda. A API está disponível publicamente para ser utilizada em projetos de estudo, testes de integração, prototipagem e aprendizado de consumo de APIs REST, eliminando a necessidade de configurar um backend completo para experimentos ou de usar dados estáticos.

## ⚡ Funcionalidades

### 🏗️ Infraestrutura como Código
Infraestrutura AWS completa provisionada via Terraform, incluindo VPC, EC2, RDS, API Gateway, Lambda e todos os recursos necessários para execução da aplicação. Versionamento e automação total da infraestrutura.

*📖 Documentação detalhada: [terraform/README.md](terraform/README.md)*

### 🤖 Atualização Automática de Dados
Lambda função executada diariamente às 03:00 UTC que regenera todos os dados fictícios do e-commerce, garantindo informações sempre atualizadas e diversificadas para estudos e testes.

*📖 Documentação detalhada: [data/README.md](data/README.md)*

### 🛍️ API REST Completa
API FastAPI com endpoints completos para gestão de produtos, clientes, fornecedores, vendas e categorias. Documentação interativa via Swagger e dados realistas para desenvolvimento e aprendizado.

A api está disponível em diferentes endpoints na URL: `https://api.gustavonucci.dev/ecomm/v1`
Os endpoints da API estão disponíveis no [swagger](https://api.gustavonucci.dev/docs)

*📖 Documentação detalhada: [api/README.md](api/README.md)*

## 🚀 Tecnologias Utilizadas

## 🚀 Tecnologias Utilizadas

### 🐍 Backend & API
- **FastAPI** - Framework web moderno para Python
- **SQLAlchemy** - ORM para Python com MySQL
- **Pydantic** - Validação de dados e serialização

### ☁️ Infraestrutura AWS
- **EC2** - Servidor de aplicação (t3.micro)
- **RDS MySQL** - Banco de dados gerenciado
- **API Gateway** - Proxy reverso e SSL
- **Lambda** - Automação serverless

### 🔄 DevOps & Automação
- **Terraform** - Infraestrutura como código
- **Docker** - Containerização da aplicação
- **GitHub Actions** - Pipeline de CI/CD

### 🛠️ Ferramentas de Desenvolvimento
- **Python 3.9+** - Linguagem principal
- **Faker** - Geração de dados fictícios
- **Git/GitHub** - Controle de versão

## 📁 Estrutura do Projeto

```
fake-ecommerce-api/
├── README.md                    # Documentação do projeto
├── app/                         # Código fonte da aplicação
│   └── src/
       ├──main.py                # Aplicação FastAPI principal
       ├──core                   # Configurações da API
       ├──models                 # Modelagem dos objetos da API (SQLAlchemy) e Schemas Pydantic
       ├──services               # Serviços vinculados à API (como healthcheck)
       └── api
          └─ routes              # As rotas da API
├── terraform/                   # Infraestrutura como código
│   ├── main.tf                  # Configuração principal
│   ├── providers.tf             # Provedores AWS
│   ├── variables.tf             # Variáveis de entrada
│   ├── outputs.tf               # Outputs da infraestrutura
│   ├── network.tf               # VPC, subnets, gateways
│   ├── security_groups.tf       # Security groups
│   ├── ec2.tf                   # Instâncias EC2
│   ├── ecr.tf                   # Repositório ECR
│   ├── rds.tf                   # Banco RDS PostgreSQL
│   ├── api_gateway.tf           # API Gateway
│   ├── lambda_update_data.tf    # Lambda responsável pela atualização dos dados diariamente
│   ├── cloud_watch.tf           # Logs e trigger da lambda
│   └── iam_roles.tf             # Roles e políticas IAM
├── .github/
│   └── workflows/
│       ├── ecr_push_and_upload.yml      # Pipeline vinculada à API
│       └── terraform.yml                # Pipeline do Terraform
├── lambda/                              # Placeholder para ser utilizado peo provisionamento da Lambda
└── data/
   ├── init_db.py                        # Inicialização do banco de dados
   ├── schema.sql                        # Schema do banco de dados
   └── update_date.py                    # Script responsável pela geração e atualização dos dados

```

## 🤝 Contribuição

Fique a vontade para contribuir com o projeto, abra sua Issue ou PR para discutirmos sobre!