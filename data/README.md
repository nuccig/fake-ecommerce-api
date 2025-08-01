# 🤖 Automação de Dados com Lambda
- **Atualização Diária Automática**
  - Lambda executada diariamente às 03:00 UTC
  - Regeneração completa de dados fictícios usando Faker
  - Limpeza e repopulação automática do banco de dados
  - Manutenção da integridade referencial entre entidades
  
- **Dados Dinâmicos e Realistas**
  - Geração de categorias com nomes e descrições variadas
  - Produtos com preços, estoques e especificações atualizadas
  - Clientes com CPFs válidos e dados demográficos realistas
  - Fornecedores com CNPJs válidos e endereços completos
  - Vendas com diferentes status e métodos de pagamento
  
- **Trigger Automático via CloudWatch**
  - Agendamento via CloudWatch Events
  - Logs detalhados de execução
  - Monitoramento de sucesso/falha da atualização
  - Integração com VPC para acesso seguro ao RDS
  
- **Benefícios para Desenvolvedores**
  - Dados sempre frescos para testes
  - Elimina necessidade de popular dados manualmente
  - Garante variedade nos dados para diferentes cenários
  - Simula ambiente real com dados em constante mudança