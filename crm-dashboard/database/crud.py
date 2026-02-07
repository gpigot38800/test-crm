"""
Opérations CRUD pour la table deals.
Fournit les fonctions d'insertion, lecture, mise à jour et suppression des données.
Supporte PostgreSQL et SQLite.
"""

import pandas as pd
from decimal import Decimal
from typing import List, Dict, Any, Optional
from .connection import get_connection, get_db_type
from .models import TABLE_NAME


def _placeholder():
    """Retourne le placeholder SQL selon le type de DB."""
    return "%s" if get_db_type() == 'postgresql' else "?"


def _convert_decimals(df: pd.DataFrame) -> pd.DataFrame:
    """Convertit les colonnes Decimal (NUMERIC PostgreSQL) en float pour la compatibilité."""
    for col in df.columns:
        if df[col].dtype == object and len(df) > 0 and isinstance(df[col].iloc[0], Decimal):
            df[col] = df[col].astype(float)
    return df


def _row_to_dict(cursor, row) -> Dict[str, Any]:
    """Convertit une row DB en dict, gère PostgreSQL et SQLite."""
    if row is None:
        return None
    if get_db_type() == 'sqlite':
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, row))
    else:
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, row))
    # Convertir les Decimal en float
    for key, value in result.items():
        if isinstance(value, Decimal):
            result[key] = float(value)
    return result


def insert_deals(deals_list: List[Dict[str, Any]]) -> int:
    """
    Insère une liste de deals en base de données (insertion batch).
    """
    if not deals_list:
        return 0

    conn = get_connection()
    cursor = conn.cursor()
    ph = _placeholder()

    try:
        columns = list(deals_list[0].keys())
        placeholders = ", ".join([ph for _ in columns])
        columns_str = ", ".join(columns)

        insert_query = f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders})"

        values = [tuple(deal.get(col) for col in columns) for deal in deals_list]

        cursor.executemany(insert_query, values)
        conn.commit()

        return len(deals_list)

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise Exception(f"Erreur lors de l'insertion des deals: {str(e)}")


def get_all_deals() -> pd.DataFrame:
    """Récupère tous les deals de la base de données."""
    try:
        conn = get_connection()
        query = f"SELECT * FROM {TABLE_NAME}"
        df = pd.read_sql_query(query, conn)
        return _convert_decimals(df)

    except Exception as e:
        raise Exception(f"Erreur lors de la lecture des deals: {str(e)}")


def get_deal_by_id(deal_id: int) -> Optional[Dict[str, Any]]:
    """Récupère un deal par son ID."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        ph = _placeholder()
        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = {ph}", (deal_id,))
        row = cursor.fetchone()
        return _row_to_dict(cursor, row)
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du deal {deal_id}: {str(e)}")


def insert_deal(deal_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Insère un deal unique et retourne le deal créé avec son id."""
    conn = get_connection()
    cursor = conn.cursor()
    ph = _placeholder()

    try:
        columns = list(deal_dict.keys())
        placeholders = ", ".join([ph for _ in columns])
        columns_str = ", ".join(columns)

        values = tuple(deal_dict.get(col) for col in columns)

        if get_db_type() == 'postgresql':
            insert_query = f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders}) RETURNING id"
            cursor.execute(insert_query, values)
            new_id = cursor.fetchone()[0]
        else:
            insert_query = f"INSERT INTO {TABLE_NAME} ({columns_str}) VALUES ({placeholders})"
            cursor.execute(insert_query, values)
            new_id = cursor.lastrowid

        conn.commit()
        return get_deal_by_id(new_id)

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise Exception(f"Erreur lors de l'insertion du deal: {str(e)}")


def update_deal(deal_id: int, deal_dict: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Met à jour un deal existant et retourne le deal modifié."""
    existing = get_deal_by_id(deal_id)
    if existing is None:
        return None

    conn = get_connection()
    cursor = conn.cursor()
    ph = _placeholder()

    try:
        set_clauses = ", ".join([f"{col} = {ph}" for col in deal_dict.keys()])
        values = list(deal_dict.values()) + [deal_id]

        update_query = f"UPDATE {TABLE_NAME} SET {set_clauses} WHERE id = {ph}"
        cursor.execute(update_query, values)
        conn.commit()

        return get_deal_by_id(deal_id)

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise Exception(f"Erreur lors de la mise à jour du deal {deal_id}: {str(e)}")


def delete_deal(deal_id: int) -> bool:
    """Supprime un deal individuel."""
    existing = get_deal_by_id(deal_id)
    if existing is None:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    ph = _placeholder()

    try:
        cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = {ph}", (deal_id,))
        conn.commit()
        return True

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise Exception(f"Erreur lors de la suppression du deal {deal_id}: {str(e)}")


def get_filtered_deals(params: Dict[str, Any]) -> pd.DataFrame:
    """Récupère les deals filtrés selon les paramètres fournis."""
    try:
        conn = get_connection()
        ph = _placeholder()
        query = f"SELECT * FROM {TABLE_NAME}"
        conditions = []
        values = []

        if params.get('statut'):
            statuts = params['statut'] if isinstance(params['statut'], list) else [params['statut']]
            placeholders = ", ".join([ph for _ in statuts])
            conditions.append(f"statut IN ({placeholders})")
            values.extend(statuts)

        if params.get('secteur'):
            secteurs = params['secteur'] if isinstance(params['secteur'], list) else [params['secteur']]
            placeholders = ", ".join([ph for _ in secteurs])
            conditions.append(f"secteur IN ({placeholders})")
            values.extend(secteurs)

        if params.get('assignee'):
            assignees = params['assignee'] if isinstance(params['assignee'], list) else [params['assignee']]
            placeholders = ", ".join([ph for _ in assignees])
            conditions.append(f"assignee IN ({placeholders})")
            values.extend(assignees)

        if params.get('date_from'):
            conditions.append(f"date_echeance >= {ph}")
            values.append(params['date_from'])

        if params.get('date_to'):
            conditions.append(f"date_echeance <= {ph}")
            values.append(params['date_to'])

        if params.get('search'):
            conditions.append(f"(LOWER(client) LIKE {ph} OR LOWER(notes) LIKE {ph})")
            search_term = f"%{params['search'].lower()}%"
            values.extend([search_term, search_term])

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        df = pd.read_sql_query(query, conn, params=values)
        return _convert_decimals(df)

    except Exception as e:
        raise Exception(f"Erreur lors de la lecture filtrée des deals: {str(e)}")


def get_filter_options() -> Dict[str, List[str]]:
    """Retourne les listes distinctes de statuts, secteurs et assignees présents en base."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT DISTINCT statut FROM {TABLE_NAME} WHERE statut IS NOT NULL AND statut != '' ORDER BY statut")
        statuts = [row[0] for row in cursor.fetchall()]

        cursor.execute(f"SELECT DISTINCT secteur FROM {TABLE_NAME} WHERE secteur IS NOT NULL AND secteur != '' ORDER BY secteur")
        secteurs = [row[0] for row in cursor.fetchall()]

        cursor.execute(f"SELECT DISTINCT assignee FROM {TABLE_NAME} WHERE assignee IS NOT NULL AND assignee != '' ORDER BY assignee")
        assignees = [row[0] for row in cursor.fetchall()]

        return {
            "statuts": statuts,
            "secteurs": secteurs,
            "assignees": assignees
        }

    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des options de filtres: {str(e)}")


def clear_all_deals() -> None:
    """Supprime tous les deals de la table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {TABLE_NAME}")
        conn.commit()

    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        raise Exception(f"Erreur lors de la suppression des deals: {str(e)}")
