"""
Module de gestion de la connexion base de données.
Supporte PostgreSQL (via DATABASE_URL) et SQLite (fallback local).
"""

import os
import sqlite3
from pathlib import Path

# Instance singleton de la connexion
_connection = None
_db_type = None  # 'postgresql' ou 'sqlite'


def get_db_type():
    """Retourne le type de base de données utilisé."""
    global _db_type
    if _db_type is None:
        _db_type = 'postgresql' if os.environ.get('DATABASE_URL') else 'sqlite'
    return _db_type


def get_connection():
    """
    Retourne une instance singleton de la connexion DB.
    Utilise PostgreSQL si DATABASE_URL est définie, sinon SQLite.
    """
    global _connection, _db_type

    db_type = get_db_type()

    if db_type == 'postgresql':
        import psycopg2
        if _connection is None or _connection.closed:
            database_url = os.environ.get('DATABASE_URL')
            # Ajouter sslmode=require si non présent (requis pour Supabase)
            if database_url and 'sslmode' not in database_url:
                separator = '&' if '?' in database_url else '?'
                database_url = f"{database_url}{separator}sslmode=require"
            _connection = psycopg2.connect(database_url)
            _connection.autocommit = False
    else:
        if _connection is None:
            db_path = Path(__file__).parent.parent / "crm_data.db"
            _connection = sqlite3.connect(str(db_path), check_same_thread=False)
            _connection.row_factory = sqlite3.Row
            _connection.execute("PRAGMA journal_mode=WAL")
            _connection.execute("PRAGMA foreign_keys=ON")

    return _connection


def init_database():
    """
    Initialise la base de données en créant le schéma.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if get_db_type() == 'sqlite':
            cursor.executescript("""
                CREATE TABLE IF NOT EXISTS deals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client TEXT NOT NULL,
                    statut TEXT NOT NULL,
                    montant_brut REAL NOT NULL,
                    probabilite REAL NOT NULL,
                    valeur_ponderee REAL NOT NULL,
                    secteur TEXT,
                    date_echeance TEXT,
                    assignee TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_deals_statut ON deals(statut);
                CREATE INDEX IF NOT EXISTS idx_deals_secteur ON deals(secteur);
                CREATE INDEX IF NOT EXISTS idx_deals_date_echeance ON deals(date_echeance);
                CREATE INDEX IF NOT EXISTS idx_deals_assignee ON deals(assignee);
            """)
            conn.commit()
        else:
            schema_path = Path(__file__).parent / "init_schema.sql"
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            cursor.execute(schema_sql)
            conn.commit()

    except Exception as e:
        if _connection:
            try:
                _connection.rollback()
            except Exception:
                pass
        raise Exception(f"Erreur lors de l'initialisation de la base de données: {str(e)}")


def close_connection():
    """Ferme proprement la connexion database."""
    global _connection
    if _connection is not None:
        try:
            _connection.close()
        except Exception:
            pass
    _connection = None
