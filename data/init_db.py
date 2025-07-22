# init_db.py

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


def init_database():
    try:

        load_dotenv()

        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")  # Note: DB_PASS, não DB_PASSWORD
        db_name = os.getenv("DB_NAME", "ecommerce")

        # Se DB_HOST não estiver definido, ler do arquivo (fallback)
        if not db_host:
            with open("../terraform/db_host.txt", "r") as file:
                db_host = file.read().strip()

        if not db_user or not db_password:
            print("Error: DB_USER and DB_PASS environment variables must be set")
            return

        print(f"Connecting to: {db_host}:{3306}/{db_name} as {db_user}")

        # Conectar ao MySQL
        connection = mysql.connector.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=3306,
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Ler e executar o schema
            with open("../data/schema.sql", "r", encoding="utf-8") as file:
                schema = file.read()

            # Executar comandos SQL
            for statement in schema.split(";"):
                statement = statement.strip()
                if statement and not statement.startswith("--"):
                    cursor.execute(statement)

            connection.commit()
            print("Database initialized successfully!")

    except Error as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        print("Error: db_host.txt file not found")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    init_database()
