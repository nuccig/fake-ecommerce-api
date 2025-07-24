# init_db.py

import os
import mysql.connector  # type: ignore
from mysql.connector import Error  # type: ignore
from dotenv import load_dotenv  # type: ignore


def init_database():
    try:

        load_dotenv()

        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME", "ecommerce")

        # Se DB_HOST não estiver definido, ler do arquivo (fallback)
        if not db_host:
            with open("../terraform/db_host.txt", "r") as file:
                db_host = file.read().strip()

        if not db_user or not db_password:
            print("Error: DB_USER and DB_PASS environment devem ser definidos")
            return

        print(f"Connecting to: {db_host}:{3306}/{db_name} as {db_user}")

        # Conecta ao MySQL
        connection = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=3306,
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Le e executar o schema
            with open("schema.sql", "r", encoding="utf-8") as file:
                schema = file.read()

            # Executa comandos SQL
            statements = []
            current_statement = ""

            for line in schema.split("\n"):
                line = line.strip()
                # Ignora linhas vazias e comentários
                if not line or line.startswith("--"):
                    continue

                current_statement += " " + line

                # Se a linha termina com ; é o fim de um comando
                if line.endswith(";"):
                    statements.append(current_statement.strip())
                    current_statement = ""

            # Executa cada comando separadamente
            for statement in statements:
                if statement:
                    try:
                        print(f"Executando: {statement[:50]}...")
                        cursor.execute(statement)
                        print("Comando executado com sucesso")
                    except Error as e:
                        print(f"Erro ao executar comando: {e}")
                        print(f"Comando: {statement}")

            connection.commit()
            print("Database iniciado com sucesso!")

    except Error as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: db_host.txt arquivo não encontrado")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    init_database()
