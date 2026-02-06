"""
Module de gestion de la connexion SQLite.
Fournit un singleton pour la connexion et l'initialisation du schéma.
"""

import sqlite3
import os
from pathlib import Path

# Chemin du fichier database (racine du projet)
DB_PATH = Path(__file__).parent.parent / "crm.db"

# Instance singleton de la connexion
_connection = None


def get_connection():
    """
    Retourne une instance singleton de la connexion SQLite.
    Configure les pragmas pour optimiser les performances.

    Returns:
        sqlite3.Connection: Instance de connexion SQLite
    """
    global _connection

    if _connection is None:
        _connection = sqlite3.connect(str(DB_PATH), check_same_thread=False)

        # Configuration des pragmas SQLite
        _connection.execute("PRAGMA foreign_keys = ON")
        _connection.execute("PRAGMA journal_mode = WAL")

        # Permet de récupérer les résultats comme des dictionnaires
        _connection.row_factory = sqlite3.Row

    return _connection


def init_database():
    """
    Initialise la base de données en exécutant le script SQL de création du schéma.
    Crée la table deals si elle n'existe pas déjà.

    Raises:
        Exception: Si l'initialisation échoue (permissions, espace disque, etc.)
    """
    try:
        conn = get_connection()

        # Lire le fichier SQL de schéma
        schema_path = Path(__file__).parent / "init_schema.sql"
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # Exécuter le script SQL
        conn.executescript(schema_sql)
        conn.commit()

    except Exception as e:
        raise Exception(f"Erreur lors de l'initialisation de la base de données: {str(e)}")


def close_connection():
    """
    Ferme proprement la connexion database.
    À appeler lors de l'arrêt de l'application.
    """
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None
