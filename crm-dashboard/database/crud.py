"""
Opérations CRUD pour la table deals.
Fournit les fonctions d'insertion, lecture et suppression des données.
"""

import pandas as pd
from typing import List, Dict, Any
from .connection import get_connection
from .models import TABLE_NAME


def insert_deals(deals_list: List[Dict[str, Any]]) -> int:
    """
    Insère une liste de deals en base de données (insertion batch).

    Args:
        deals_list: Liste de dictionnaires contenant les données des deals

    Returns:
        int: Nombre de deals insérés

    Raises:
        Exception: Si l'insertion échoue
    """
    if not deals_list:
        return 0

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Récupérer les colonnes du premier deal (toutes doivent avoir les mêmes colonnes)
        columns = list(deals_list[0].keys())
        placeholders = ", ".join(["?" for _ in columns])
        columns_str = ", ".join(columns)

        insert_query = f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders})"

        # Préparer les valeurs pour l'insertion batch
        values = [tuple(deal.get(col) for col in columns) for deal in deals_list]

        # Insertion batch
        cursor.executemany(insert_query, values)
        conn.commit()

        return len(deals_list)

    except Exception as e:
        conn.rollback()
        raise Exception(f"Erreur lors de l'insertion des deals: {str(e)}")


def get_all_deals() -> pd.DataFrame:
    """
    Récupère tous les deals de la base de données.

    Returns:
        pd.DataFrame: DataFrame pandas contenant tous les deals

    Raises:
        Exception: Si la lecture échoue
    """
    try:
        conn = get_connection()
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(query, conn)
        return df

    except Exception as e:
        raise Exception(f"Erreur lors de la lecture des deals: {str(e)}")


def clear_all_deals() -> None:
    """
    Supprime tous les deals de la table (TRUNCATE).
    Utilisé avant chaque nouvel import CSV.

    Raises:
        Exception: Si la suppression échoue
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise Exception(f"Erreur lors de la suppression des deals: {str(e)}")
