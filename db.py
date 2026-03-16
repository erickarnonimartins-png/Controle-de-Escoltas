from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "escolta.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS agentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        pix TEXT,
        observacao TEXT,
        ativo INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rotas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_rota TEXT NOT NULL,
        origem TEXT,
        destino TEXT,
        valor_fixo_receber REAL NOT NULL DEFAULT 0,
        valor_fixo_pagar REAL NOT NULL DEFAULT 0,
        observacao TEXT,
        ativa INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_servico TEXT NOT NULL,
        rota_id INTEGER NOT NULL,
        agente_id INTEGER NOT NULL,
        placa_caminhao TEXT,
        hora_inicial TEXT,
        hora_final TEXT,
        total_horas REAL DEFAULT 0,
        valor_fixo_receber REAL DEFAULT 0,
        valor_fixo_pagar REAL DEFAULT 0,
        valor_extra_recebido REAL DEFAULT 0,
        pedagio_km_extra REAL DEFAULT 0,
        total_receber REAL DEFAULT 0,
        total_pagar REAL DEFAULT 0,
        lucro REAL DEFAULT 0,
        observacao TEXT,
        status_pagamento TEXT DEFAULT 'pendente',
        data_pagamento TEXT,
        forma_pagamento TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (rota_id) REFERENCES rotas (id),
        FOREIGN KEY (agente_id) REFERENCES agentes (id)
    )
    """)

    conn.commit()
    conn.close()
