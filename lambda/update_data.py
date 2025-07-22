import json
import pymysql
import os
from faker import Faker
from faker_commerce import Provider
from dotenv import load_dotenv

fake = Faker()
fake.add_provider(Provider)


def insert_fake_data(cursor):
    # Inserir clientes
    for _ in range(5):
        cursor.execute(
            "INSERT INTO clientes (nome, email, cidade, estado) VALUES (%s, %s, %s, %s)",
            (fake.name(), fake.email(), fake.city(), fake.state_abbr()),
        )

    # Inserir produtos
    for _ in range(1):
        cursor.execute(
            "INSERT INTO produtos (nome, categoria, preco, em_estoque) VALUES (%s, %s, %s, %s)",
            (
                fake.product_name(),
                fake.category(),
                round(fake.random_number(digits=2), 2),
                fake.random_boolean(),
            ),
        )

    # Inserir vendas
    for _ in range(10):
        cursor.execute(
            "INSERT INTO vendas (cliente_id, data_venda, total) VALUES (%s, %s, %s)",
            (
                fake.random_int(min=1, max=5),
                fake.date_this_year(),
                round(fake.random_number(digits=2), 2),
            ),
        )

    # Inserir itens de venda
    for _ in range(15):
        cursor.execute(
            "INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unit) VALUES (%s, %s, %s, %s)",
            (
                fake.random_int(min=1, max=5),
                fake.random_int(min=1, max=20),
                fake.random_int(min=1, max=5),
                round(fake.random_number(digits=2), 2),
            ),
        )


def lambda_handler(event, context):

    load_dotenv()

    # Configurações do banco de dados
    db_config = {
        "host": os.environ.get("DB_HOST"),
        "user": os.environ.get("DB_USER", "admin"),
        "password": os.environ.get("DB_PASSWORD"),
        "database": os.environ.get("DB_NAME", "ecommerce"),
        "charset": "utf8mb4",
        "autocommit": True,
    }

    if not db_config["host"]:
        with open("../terraform/db_host.txt", "r") as file:
            db_config["host"] = file.read().strip()

    if not db_config["user"] or not db_config["password"]:
        print("Error: DB_USER and DB_PASS environment variables must be set")
        return

    print(
        f"Connecting to: {db_config['host']}:{3306}/{db_config['database']} as {db_config['user']}"
    )

    try:
        # Conectar ao banco
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()

        # Inserir dados fake
        insert_fake_data(cursor)

        connection.commit()
        cursor.close()
        connection.close()

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Dados inseridos com sucesso!",
                    "timestamp": fake.iso8601(),
                }
            ),
        }

    except Exception as e:
        print(f"Erro: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }
