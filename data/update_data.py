import json
import os
import random
from datetime import datetime

import pymysql  # type: ignore
from dotenv import load_dotenv  # type: ignore
from faker import Faker  # type: ignore

fake = Faker("pt_BR")


class Generator:

    def __init__(self):
        pass

    # FORNECEDORES
    def gerar_fornecedor(self):
        return {
            "nome": fake.company(),
            "email": fake.company_email(),
            "telefone": fake.phone_number(),
            "cnpj": fake.cnpj(),  # Requer faker brasileira
            "endereco": fake.address(),
            "cidade": fake.city(),
            "estado": fake.state_abbr(),
            "cep": fake.postcode(),
            "ativo": random.choice([True, False]),
        }

    # CATEGORIAS
    def gerar_categoria(self):
        categorias = [
            "Eletrônicos",
            "Roupas",
            "Casa e Jardim",
            "Esportes",
            "Livros",
            "Beleza",
            "Automóveis",
            "Brinquedos",
            "Alimentação",
            "Saúde",
        ]
        return {
            "nome": random.choice(categorias),
            "descricao": fake.text(max_nb_chars=200),
            "ativa": random.choice([True, False]),
        }

    # CLIENTES
    def gerar_cliente(self):
        return {
            "nome": fake.first_name(),
            "sobrenome": fake.last_name(),
            "email": fake.email(),
            "telefone": fake.phone_number(),
            "cpf": fake.cpf(),  # Requer faker brasileira
            "data_nascimento": fake.date_of_birth(minimum_age=18, maximum_age=80),
            "genero": random.choice(["M", "F", "Outro"]),
        }

    # ENDEREÇOS
    def gerar_endereco(self, cliente_id):
        return {
            "cliente_id": cliente_id,
            "cep": fake.postcode(),
            "logradouro": fake.street_name(),
            "numero": fake.building_number(),
            "complemento": (
                random.choice(
                    [
                        f"Apto {random.randint(1, 999)}",
                        f"Bloco {random.choice(['A', 'B', 'C', 'D'])}",
                        f"Casa {random.randint(1, 20)}",
                        f"Sala {random.randint(101, 999)}",
                        "Fundos",
                        "Térreo",
                    ]
                )
                if random.choice([True, False])
                else None
            ),
            "bairro": fake.neighborhood(),
            "cidade": fake.city(),
            "estado": fake.state_abbr(),
            "endereco_principal": random.choice([True, False]),
        }

    # PRODUTOS
    def gerar_produto(self, categoria_id, fornecedor_id):

        produtos = [
            "Smartphone",
            "Notebook",
            "Camiseta",
            "Tênis",
            "Livro",
            "Perfume",
            "Relógio",
            "Fone de Ouvido",
            "Mochila",
            "Mesa",
        ]
        nome_produto = random.choice(produtos)

        preco = round(random.uniform(10.00, 1000.00), 2)
        custo = round(preco * random.uniform(0.4, 0.7), 2)

        return {
            "nome": nome_produto,
            "descricao": fake.text(max_nb_chars=300),
            "categoria_id": categoria_id,
            "fornecedor_id": fornecedor_id,
            "preco": preco,
            "custo": custo,
            "peso": round(random.uniform(0.1, 10.0), 3),
            "quantidade_estoque": random.randint(0, 100),
            "em_estoque": random.choice([True, False]),
            "ativo": random.choice([True, False]),
        }

    # VENDAS
    def gerar_venda(self, cliente_id, endereco_id):
        subtotal = round(random.uniform(50.00, 500.00), 2)
        frete = round(random.uniform(5.00, 30.00), 2)

        return {
            "cliente_id": cliente_id,
            "endereco_entrega_id": endereco_id,
            "status": random.choice(
                ["Pendente", "Confirmado", "Enviado", "Entregue", "Cancelado"]
            ),
            "subtotal": subtotal,
            "frete": frete,
            "total": subtotal + frete,
            "metodo_pagamento": random.choice(
                ["Cartao_Credito", "Cartao_Debito", "PIX", "Boleto"]
            ),
            "status_pagamento": random.choice(["Pendente", "Aprovado", "Recusado"]),
            "data_venda": datetime.now(),
            "data_entrega_prevista": fake.date_between(
                start_date="today", end_date="+30d"
            ),
        }

    # ITENS VENDA
    def gerar_item_venda(self, venda_id, produto_id):
        quantidade = random.randint(1, 5)
        preco_unitario = round(random.uniform(10.00, 200.00), 2)

        return {
            "venda_id": venda_id,
            "produto_id": produto_id,
            "quantidade": quantidade,
            "preco_unitario": preco_unitario,
            "subtotal": quantidade * preco_unitario,
        }


def insert_fake_data(cursor):
    generator = Generator()

    try:
        cursor.execute("SELECT MAX(id) FROM fornecedores")
        max_fornecedor_id = cursor.fetchone()[0] or 0
    except pymysql.Error as e:
        print(f"Erro ao obter o ID máximo de fornecedores: {e}")
        max_fornecedor_id = 0

    try:
        cursor.execute("SELECT MAX(id) FROM categorias")
        max_categoria_id = cursor.fetchone()[0] or 0
    except pymysql.Error as e:
        print(f"Erro ao obter o ID máximo de categorias: {e}")
        max_categoria_id = 0

    if max_categoria_id == 0:
        print("Primeira execução: criando categorias iniciais...")
        categorias_unicas = set()
        for _ in range(10):  # Tentar inserir até 10 categorias únicas
            categoria = generator.gerar_categoria()
            if categoria["nome"] not in categorias_unicas:
                categorias_unicas.add(categoria["nome"])
                try:
                    cursor.execute(
                        """
                        INSERT INTO categorias (nome, descricao, ativa) 
                        VALUES (%s, %s, %s)
                    """,
                        (categoria["nome"], categoria["descricao"], categoria["ativa"]),
                    )
                except pymysql.IntegrityError:
                    pass
        # Atualizar max_categoria_id
        cursor.execute("SELECT MAX(id) FROM categorias")
        max_categoria_id = cursor.fetchone()[0] or 0

    if max_fornecedor_id == 0:
        print("Primeira execução: criando fornecedores iniciais...")
        for _ in range(5):
            fornecedor = generator.gerar_fornecedor()
            try:
                cursor.execute(
                    """
                    INSERT INTO fornecedores (nome, email, telefone, cnpj, endereco, cidade, estado, cep, ativo) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        fornecedor["nome"],
                        fornecedor["email"],
                        fornecedor["telefone"],
                        fornecedor["cnpj"],
                        fornecedor["endereco"],
                        fornecedor["cidade"],
                        fornecedor["estado"],
                        fornecedor["cep"],
                        fornecedor["ativo"],
                    ),
                )
            except pymysql.IntegrityError:
                pass
        # Atualizar max_fornecedor_id
        cursor.execute("SELECT MAX(id) FROM fornecedores")
        max_fornecedor_id = cursor.fetchone()[0] or 0

    if random.random() < 0.2:
        print("Adicionando novo fornecedor...")
        fornecedor = generator.gerar_fornecedor()
        try:
            cursor.execute(
                """
                INSERT INTO fornecedores (nome, email, telefone, cnpj, endereco, cidade, estado, cep, ativo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    fornecedor["nome"],
                    fornecedor["email"],
                    fornecedor["telefone"],
                    fornecedor["cnpj"],
                    fornecedor["endereco"],
                    fornecedor["cidade"],
                    fornecedor["estado"],
                    fornecedor["cep"],
                    fornecedor["ativo"],
                ),
            )
            max_fornecedor_id = cursor.lastrowid
        except pymysql.IntegrityError:
            pass

    novos_clientes = []
    num_novos_clientes = random.randint(3, 8)
    print(f"Registrando {num_novos_clientes} novos clientes...")

    for _ in range(num_novos_clientes):
        cliente = generator.gerar_cliente()
        try:
            cursor.execute(
                """
                INSERT INTO clientes (nome, sobrenome, email, telefone, cpf, data_nascimento, genero) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    cliente["nome"],
                    cliente["sobrenome"],
                    cliente["email"],
                    cliente["telefone"],
                    cliente["cpf"],
                    cliente["data_nascimento"],
                    cliente["genero"],
                ),
            )
            novos_clientes.append(cursor.lastrowid)
        except pymysql.IntegrityError:
            # Email ou CPF já existe, tentar novamente
            pass

    for cliente_id in novos_clientes:
        endereco = generator.gerar_endereco(cliente_id)
        cursor.execute(
            """
            INSERT INTO enderecos (cliente_id, cep, logradouro, numero, complemento, bairro, cidade, estado, endereco_principal) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                endereco["cliente_id"],
                endereco["cep"],
                endereco["logradouro"],
                endereco["numero"],
                endereco["complemento"],
                endereco["bairro"],
                endereco["cidade"],
                endereco["estado"],
                endereco["endereco_principal"],
            ),
        )

    novos_produtos = []
    num_novos_produtos = random.randint(2, 5)
    print(f"Adicionando {num_novos_produtos} novos produtos...")

    cursor.execute("SELECT id FROM categorias WHERE ativa = TRUE")
    categorias_ativas = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM fornecedores WHERE ativo = TRUE")
    fornecedores_ativos = [row[0] for row in cursor.fetchall()]

    if categorias_ativas and fornecedores_ativos:
        for _ in range(num_novos_produtos):
            produto = generator.gerar_produto(
                categoria_id=random.choice(categorias_ativas),
                fornecedor_id=random.choice(fornecedores_ativos),
            )
            cursor.execute(
                """
                INSERT INTO produtos (nome, descricao, categoria_id, fornecedor_id, preco, custo, peso, quantidade_estoque, em_estoque, ativo) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    produto["nome"],
                    produto["descricao"],
                    produto["categoria_id"],
                    produto["fornecedor_id"],
                    produto["preco"],
                    produto["custo"],
                    produto["peso"],
                    produto["quantidade_estoque"],
                    produto["em_estoque"],
                    produto["ativo"],
                ),
            )
            novos_produtos.append(cursor.lastrowid)
    else:
        print("Erro: Não há categorias ou fornecedores ativos para criar produtos")

    novos_vendas = []
    num_vendas = random.randint(5, 15)
    print(f"Processando {num_vendas} vendas de hoje...")

    cursor.execute("SELECT id FROM clientes")
    todos_clientes = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT COUNT(*) FROM produtos WHERE ativo = TRUE")
    produtos_ativos_count = cursor.fetchone()[0]

    if todos_clientes and produtos_ativos_count > 0:
        for _ in range(num_vendas):
            # Clientes novos têm maior probabilidade de comprar (simulando campanhas)
            if novos_clientes and random.random() < 0.4:
                cliente_id = random.choice(novos_clientes)
            else:
                cliente_id = random.choice(todos_clientes)

            # Buscar endereço do cliente
            cursor.execute(
                "SELECT id FROM enderecos WHERE cliente_id = %s ORDER BY RAND() LIMIT 1",
                (cliente_id,),
            )
            endereco_result = cursor.fetchone()
            endereco_id = endereco_result[0] if endereco_result else None

            venda = generator.gerar_venda(cliente_id, endereco_id)
            cursor.execute(
                """
                INSERT INTO vendas (cliente_id, endereco_entrega_id, status, subtotal, frete, total, metodo_pagamento, status_pagamento, data_entrega_prevista) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    venda["cliente_id"],
                    venda["endereco_entrega_id"],
                    venda["status"],
                    venda["subtotal"],
                    venda["frete"],
                    venda["total"],
                    venda["metodo_pagamento"],
                    venda["status_pagamento"],
                    venda["data_entrega_prevista"],
                ),
            )
            novos_vendas.append(cursor.lastrowid)
    else:
        print("Aviso: Não há clientes ou produtos ativos suficientes para criar vendas")

    cursor.execute("SELECT id FROM produtos WHERE ativo = TRUE")
    todos_produtos = [row[0] for row in cursor.fetchall()]

    if todos_produtos:
        for venda_id in novos_vendas:
            # Cada venda terá 1-4 produtos diferentes
            num_itens = random.randint(1, 4)
            produtos_na_venda = random.sample(
                todos_produtos, min(num_itens, len(todos_produtos))
            )

            for produto_id in produtos_na_venda:
                item_venda = generator.gerar_item_venda(venda_id, produto_id)
                cursor.execute(
                    """
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario, subtotal) 
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    (
                        item_venda["venda_id"],
                        item_venda["produto_id"],
                        item_venda["quantidade"],
                        item_venda["preco_unitario"],
                        item_venda["subtotal"],
                    ),
                )
    else:
        print("Aviso: Não há produtos ativos para criar itens de venda")

    print(
        f"RESUMO DO DIA: {len(novos_clientes)} novos clientes, {len(novos_produtos)} novos produtos, {len(novos_vendas)} vendas realizadas"
    )

    return {
        "novos_clientes": len(novos_clientes),
        "novos_produtos": len(novos_produtos),
        "vendas_realizadas": len(novos_vendas),
        "total_itens_vendidos": (
            sum(
                len(
                    random.sample(
                        todos_produtos, min(random.randint(1, 4), len(todos_produtos))
                    )
                )
                for _ in novos_vendas
            )
            if todos_produtos
            else 0
        ),
    }


def lambda_handler(event, context):
    start_time = datetime.now()

    load_dotenv()

    db_config = {
        "host": os.environ.get("DB_HOST"),
        "user": os.environ.get("DB_USER", "admin"),
        "password": os.environ.get("DB_PASSWORD"),
        "database": os.environ.get("DB_NAME", "ecommerce"),
        "charset": "utf8mb4",
        "autocommit": False,
        "connect_timeout": 30,
        "read_timeout": 30,
        "write_timeout": 30,
    }

    # Fallback para host via arquivo (se não estiver nas env vars)
    if not db_config["host"]:
        try:
            with open("./db_host.txt", "r") as file:
                db_config["host"] = file.read().strip()
        except FileNotFoundError:
            print("Erro: Arquivo db_host.txt não encontrado e DB_HOST não definido")
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "Configuração de host do banco não encontrada"}
                ),
            }

    if not db_config["host"]:
        print("Erro: DB_HOST não configurado")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "DB_HOST é obrigatório"}),
        }

    if not db_config["password"]:
        print("Erro: DB_PASSWORD não configurado")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "DB_PASSWORD é obrigatório"}),
        }

    print(
        f"Iniciando conexão com: {db_config['host']}:{3306}/{db_config['database']} as {db_config['user']}"
    )

    connection = None
    cursor = None

    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT 1")
        print("Conexão com banco estabelecida com sucesso")

        dados_inseridos = insert_fake_data(cursor)

        connection.commit()
        print("Transação commitada com sucesso")

        execution_time = (datetime.now() - start_time).total_seconds()

        response_body = {
            "message": "Dados inseridos com sucesso!",
            "timestamp": datetime.now().isoformat(),
            "execution_time_seconds": round(execution_time, 2),
            "database_host": db_config["host"],
            "database_name": db_config["database"],
            "summary": dados_inseridos or "Dados processados",
        }

        print(f"Execução completada em {execution_time:.2f} segundos")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response_body, ensure_ascii=False),
        }

    except pymysql.MySQLError as e:
        error_msg = f"Erro MySQL: {str(e)}"
        print(error_msg)

        if connection:
            try:
                connection.rollback()
                print("Rollback realizado")
            except:
                pass

        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "error": "Erro de banco de dados",
                    "details": str(e),
                    "timestamp": datetime.now().isoformat(),
                },
                ensure_ascii=False,
            ),
        }

    except Exception as e:
        error_msg = f"Erro geral: {str(e)}"
        print(error_msg)

        if connection:
            try:
                connection.rollback()
                print("Rollback realizado")
            except:
                pass

        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(
                {
                    "error": "Erro interno do servidor",
                    "details": str(e),
                    "timestamp": datetime.now().isoformat(),
                },
                ensure_ascii=False,
            ),
        }

    finally:
        # Sempre fecha as conexões
        if cursor:
            try:
                cursor.close()
                print("Cursor fechado")
            except:
                pass

        if connection:
            try:
                connection.close()
                print("Conexão fechada")
            except:
                pass
