from database import Database

# Lista das tabelas que você quer buscar todas as colunas
TABLES_TO_FETCH = [
    "acolhimento_urgencia_emergencia",
    "paciente",
    "medico",
    "classificacao_risco_acolhimento"
]

def get_table_columns(schema: str, tables: list):
    """Busca todas as colunas apenas das tabelas desejadas no schema informado."""
    db = Database()
    conn = db.get_connection()

    try:
        with conn.cursor() as cur:
            # Filtra as colunas apenas das tabelas especificadas
            query = f"""
                SELECT table_name, column_name 
                FROM information_schema.columns 
                WHERE table_schema = %s AND table_name IN ({", ".join(['%s'] * len(tables))})
                ORDER BY table_name, ordinal_position;
            """
            cur.execute(query, [schema] + tables)
            
            table_columns = {}
            for table, column in cur.fetchall():
                if table not in table_columns:
                    table_columns[table] = []
                table_columns[table].append(column)

            return table_columns
    finally:
        db.release_connection(conn)

def fetch_data(schema: str):
    """Captura dados apenas das tabelas selecionadas e com todas as colunas."""
    table_columns = get_table_columns(schema, TABLES_TO_FETCH)
    queries = []
    
    for table, columns in table_columns.items():
        cols = ", ".join(columns)  # Pega todas as colunas da tabela
        queries.append(f"SELECT {cols} FROM {schema}.{table}")

    if not queries:
        return []

    full_query = " UNION ALL ".join(queries)

    db = Database()
    conn = db.get_connection()
    
    try:
        with conn.cursor() as cur:
            cur.execute(full_query)
            data = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in data]
    except Exception as e:
        print(f"❌ Erro na consulta: {e}")
        return []
    finally:
        db.release_connection(conn)  # Devolve a conexão ao pool

# Exemplo de uso
schema = "public"
dados = fetch_data(schema)
print(dados)
