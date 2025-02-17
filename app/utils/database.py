import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.db_pool = None
        self.create_pool()

    def create_pool(self):
        """ cria um pool de conexões para otimizar o acesso ao banco. """
        try:
            self.db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                client_encoding="LATIN1"
            )
            if self.db_pool:
                print("✅ Pool de conexões criado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar pool de conexões: {e}")

    def get_connection(self):
        """ obtém uma conexão do pool. """
        try:
            if self.db_pool:
                return self.db_pool.getconn()
        except Exception as e:
            print(f"❌ Erro ao obter conexão: {e}")
        return None

    def release_connection(self, conn):
        """ devolve a conexão ao pool. """
        if self.db_pool and conn:
            self.db_pool.putconn(conn)

    def close_pool(self):
        """ fecha todas as conexões no pool. """
        if self.db_pool:
            self.db_pool.closeall()
            print("🛑 Pool de conexões fechado.")

# testando a conexão
if __name__ == "__main__":
    db = Database()
    conn = db.get_connection()
    
    if conn:
        print("✅ Conexão com PostgreSQL bem-sucedida!")
        db.release_connection(conn)  # devolve a conexão ao pool
    else:
        print("❌ Falha ao conectar ao banco.")

