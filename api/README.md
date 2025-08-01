## 📁 A API
A api está disponível em diferentes endpoints na URL https://api.gustavonucci.dev/ecomm/v1
Os endpoints da API estão disponíveis no [swagger](https://api.gustavonucci.dev/docs)

## 🌐 Endpoints da API

Os endpoints da API estão disponíveis no [swagger](https://api.gustavonucci.dev/docs)

### 📊 Health Check
- `GET /health` - Status da aplicação e conectividade do banco

### 🏷️ Categorias
- `GET /categories` - Listar todas as categorias
- `POST /categories` - Criar nova categoria
- `GET /categories/{category_id}` - Obter categoria específica
- `PUT /categories/{category_id}` - Atualizar categoria
- `DELETE /categories/{category_id}` - Excluir categoria
- `GET /categories/search` - Buscar categorias (por nome ou descrição)

### 📦 Produtos
- `GET /products` - Listar todos os produtos
- `POST /products` - Criar novo produto
- `GET /products/{product_id}` - Obter produto específico
- `PUT /products/{product_id}` - Atualizar produto
- `DELETE /products/{product_id}` - Excluir produto
- `GET /products/search` - Buscar produtos (por nome ou categoria)
- `GET /products/category/{category_id}` - Listar produtos por categoria

### 👥 Clientes
- `GET /customers` - Listar todos os clientes
- `POST /customers` - Criar novo cliente
- `GET /customers/{customer_id}` - Obter cliente específico
- `PUT /customers/{customer_id}` - Atualizar cliente
- `DELETE /customers/{customer_id}` - Excluir cliente
- `GET /customers/search` - Buscar clientes (por nome, CPF ou email)

### 🏭 Fornecedores
- `GET /suppliers` - Listar todos os fornecedores
- `POST /suppliers` - Criar novo fornecedor
- `GET /suppliers/{supplier_id}` - Obter fornecedor específico
- `PUT /suppliers/{supplier_id}` - Atualizar fornecedor
- `DELETE /suppliers/{supplier_id}` - Excluir fornecedor
- `GET /suppliers/search` - Buscar fornecedores (por nome, CNPJ ou email)

### 📍 Endereços
- `GET /addresses` - Listar todos os endereços
- `POST /addresses` - Criar novo endereço
- `GET /addresses/{address_id}` - Obter endereço específico
- `PUT /addresses/{address_id}` - Atualizar endereço
- `DELETE /addresses/{address_id}` - Excluir endereço
- `GET /addresses/customer/{customer_id}` - Listar endereços de um cliente
- `GET /addresses/search` - Buscar endereços (por CEP, logradouro ou cliente)

### 🛒 Vendas
- `GET /sales` - Listar todas as vendas
- `POST /sales` - Criar nova venda
- `GET /sales/{sale_id}` - Obter venda específica
- `PUT /sales/{sale_id}` - Atualizar venda
- `DELETE /sales/{sale_id}` - Excluir venda
- `GET /sales/customer/{customer_id}` - Listar vendas de um cliente
- `GET /sales/search` - Buscar vendas (por status, método de pagamento, etc.)

### 📋 Itens de Venda
- `GET /sale-items` - Listar todos os itens de venda
- `POST /sale-items` - Adicionar item à venda
- `GET /sale-items/{item_id}` - Obter item específico
- `PUT /sale-items/{item_id}` - Atualizar item de venda
- `DELETE /sale-items/{item_id}` - Remover item de venda
- `GET /sale-items/sale/{sale_id}` - Listar itens de uma venda específica

### 📝 Documentação Interativa
- `GET /docs` - Interface Swagger UI
- `GET /redoc` - Documentação ReDoc
- `GET /openapi.json` - Schema OpenAPI

## Database Schema
<img width="1343" height="1088" alt="Fake API ecommerce (1)" src="https://github.com/user-attachments/assets/92533b96-e8c2-4fb4-a735-d598061e8063" /> 
