"""
Fonctions de transformation et mapping des données CSV.
Normalise les colonnes et mappe vers le schéma database.
"""

import pandas as pd
from utils.constants import CSV_TO_DB_COLUMNS


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalise les noms de colonnes du DataFrame (lowercase, strip whitespace).

    Args:
        df: DataFrame avec colonnes non normalisées

    Returns:
        pd.DataFrame: DataFrame avec colonnes normalisées
    """
    # Créer une copie pour ne pas modifier l'original
    df_normalized = df.copy()

    # Normaliser: minuscules + strip whitespace
    df_normalized.columns = [col.lower().strip() for col in df_normalized.columns]

    return df_normalized


def map_csv_to_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mappe les colonnes CSV vers les colonnes du schéma database.

    Args:
        df: DataFrame avec colonnes CSV normalisées

    Returns:
        pd.DataFrame: DataFrame avec colonnes DB

    Examples:
        Input columns: ['client', 'statut', 'montant', 'tags', 'date échéance']
        Output columns: ['client', 'statut', 'montant_brut', 'secteur', 'date_echeance']
    """
    # Créer une copie
    df_mapped = df.copy()

    # Renommer les colonnes selon le mapping
    rename_dict = {}
    for csv_col, db_col in CSV_TO_DB_COLUMNS.items():
        if csv_col in df_mapped.columns:
            rename_dict[csv_col] = db_col

    df_mapped = df_mapped.rename(columns=rename_dict)

    return df_mapped
