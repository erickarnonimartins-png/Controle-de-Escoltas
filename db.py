from pathlib import Path
import sqlite3

import streamlit as st

DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
SQLITE_PATH = DB_DIR / "escolta.db"


def get_connection():
    database_url = st.secrets.get("DATABASE_URL", "")

    if database_url:
        try:
            import psycopg
            conn = psycopg.connect(database_url)
            conn.row_factory = psycopg.rows.dict_row
            return conn
        except Exception as e:
            raise RuntimeError(f"Erro ao conectar no banco online: {e}")

    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS agentes (
        id SERIAL PRIMARY KEY,
        nome TEXT NOT NULL,
        telefone TEXT,
        pix TEXT,
        observacao TEXT,
        ativo INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rotas (
        id SERIAL PRIMARY KEY,
        nome_rota TEXT NOT NULL,
        origem TEXT,
        destino TEXT,
        valor_fixo_receber NUMERIC DEFAULT 0,
        valor_fixo_pagar NUMERIC DEFAULT 0,
        observacao TEXT,
        ativa INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS servicos (
        id SERIAL PRIMARY KEY,
        data_servico TEXT NOT NULL,
        rota_id INTEGER NOT NULL,
        agente_id INTEGER NOT NULL,
        placa_caminhao TEXT,
        hora_inicial TEXT,
        hora_final TEXT,
        total_horas NUMERIC DEFAULT 0,
        valor_fixo_receber NUMERIC DEFAULT 0,
        valor_fixo_pagar NUMERIC DEFAULT 0,
        valor_extra_recebido NUMERIC DEFAULT 0,
        pedagio_km_extra NUMERIC DEFAULT 0,
        total_receber NUMERIC DEFAULT 0,
        total_pagar NUMERIC DEFAULT 0,
        lucro NUMERIC DEFAULT 0,
        observacao TEXT,
        status_pagamento TEXT DEFAULT 'pendente',
        data_pagamento TEXT,
        forma_pagamento TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
