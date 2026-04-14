import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cod TEXT,
            categoria TEXT,
            marca TEXT,
            preco REAL,
            preco_venda REAL,
            qtd_estoque INTEGER,
            min_estoque INTEGER,
            unidade TEXT
        )
    ''')
    conn.commit()
    conn.close()