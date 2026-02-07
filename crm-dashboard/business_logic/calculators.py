"""
Fonctions de calcul métier.
Calcule les probabilités, valeurs pondérées et le pipeline total.
"""

import pandas as pd
from typing import Union, List, Dict, Any
from datetime import datetime, timedelta
import logging
from utils.constants import PROBABILITY_MAP, COLD_DEAL_THRESHOLD_DAYS, WON_STATUSES

# Configuration du logger
logger = logging.getLogger(__name__)


def calculate_probability(statut: str) -> float:
    """
    Calcule la probabilité de conversion selon le statut du deal.

    Args:
        statut: Statut du deal (Prospect, Qualifié, Négociation, Gagné)

    Returns:
        float: Probabilité de conversion (0.10, 0.30, 0.70, 1.00)
              Par défaut 0.10 si statut non reconnu
    """
    # Normaliser le statut (minuscules, strip whitespace)
    normalized_statut = statut.lower().strip()

    # Récupérer la probabilité depuis le mapping
    probability = PROBABILITY_MAP.get(normalized_statut, 0.10)

    # Log warning si statut non reconnu
    if normalized_statut not in PROBABILITY_MAP:
        logger.warning(f"Statut non reconnu: '{statut}'. Probabilité par défaut: 0.10")

    return probability


def calculate_weighted_value(montant_brut: float, probabilite: float) -> float:
    """
    Calcule la valeur pondérée d'un deal.

    Args:
        montant_brut: Montant total du deal
        probabilite: Probabilité de conversion (0.10 à 1.00)

    Returns:
        float: Valeur pondérée arrondie à 2 décimales
    """
    return round(montant_brut * probabilite, 2)


def calculate_total_pipeline(deals_df: pd.DataFrame) -> float:
    """
    Calcule le pipeline pondéré total (somme des valeurs pondérées).

    Args:
        deals_df: DataFrame contenant les deals avec colonne 'valeur_ponderee'

    Returns:
        float: Pipeline pondéré total. Retourne 0 si DataFrame vide ou colonne manquante
    """
    # Vérifier si le DataFrame est vide
    if deals_df.empty:
        return 0.0

    # Vérifier si la colonne valeur_ponderee existe
    if 'valeur_ponderee' not in deals_df.columns:
        logger.warning("Colonne 'valeur_ponderee' manquante dans le DataFrame")
        return 0.0

    # Calculer la somme
    total = deals_df['valeur_ponderee'].sum()

    return round(total, 2)


def calculate_performance_by_assignee(deals_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Calcule les métriques de performance par commercial (assignee).

    Args:
        deals_df: DataFrame contenant les deals

    Returns:
        Liste de dicts avec nb_deals, montant_total, pipeline_pondere,
        deals_gagnes, taux_conversion, panier_moyen par assignee
    """
    if deals_df.empty:
        return []

    # Remplacer les assignees vides par "Non assigné"
    df = deals_df.copy()
    df['assignee'] = df['assignee'].fillna('Non assigné').replace('', 'Non assigné')

    results = []
    for assignee, group in df.groupby('assignee'):
        nb_deals = len(group)
        montant_total = round(group['montant_brut'].sum(), 2)
        pipeline_pondere = round(group['valeur_ponderee'].sum(), 2) if 'valeur_ponderee' in group.columns else 0.0
        deals_gagnes = len(group[group['statut'].str.lower().str.strip().isin(['gagné', 'gagné - en cours'])])
        taux_conversion = round((deals_gagnes / nb_deals) * 100, 1) if nb_deals > 0 else 0.0
        panier_moyen = round(group['montant_brut'].mean(), 2)

        results.append({
            "assignee": assignee,
            "nb_deals": nb_deals,
            "montant_total": montant_total,
            "pipeline_pondere": pipeline_pondere,
            "deals_gagnes": deals_gagnes,
            "taux_conversion": taux_conversion,
            "panier_moyen": panier_moyen
        })

    # Trier par pipeline pondéré décroissant
    results.sort(key=lambda x: x['pipeline_pondere'], reverse=True)

    return results


def calculate_sales_velocity(deals_df: pd.DataFrame) -> float:
    """
    Calcule la durée moyenne de conversion en jours pour les deals "Gagné".
    Basé sur updated_at - created_at.

    Returns:
        float: Durée moyenne en jours, 0 si aucun deal gagné
    """
    if deals_df.empty:
        return 0.0

    df = deals_df.copy()
    won = df[df['statut'].str.lower().str.strip().isin(WON_STATUSES)]

    if won.empty:
        return 0.0

    try:
        created = pd.to_datetime(won['created_at'], errors='coerce')
        updated = pd.to_datetime(won['updated_at'], errors='coerce')
        durations = (updated - created).dt.total_seconds() / 86400  # en jours
        durations = durations.dropna()
        durations = durations[durations >= 0]

        if durations.empty:
            return 0.0

        return round(durations.mean(), 1)
    except Exception as e:
        logger.warning(f"Erreur calcul vélocité: {e}")
        return 0.0


def calculate_velocity_by_group(deals_df: pd.DataFrame, group_col: str) -> Dict[str, float]:
    """
    Ventile la vitesse de vente par groupe (secteur ou commercial).

    Returns:
        Dict mapping groupe → durée moyenne en jours
    """
    if deals_df.empty:
        return {}

    df = deals_df.copy()
    won = df[df['statut'].str.lower().str.strip().isin(WON_STATUSES)]

    if won.empty or group_col not in won.columns:
        return {}

    try:
        won = won.copy()
        won['created_at_dt'] = pd.to_datetime(won['created_at'], errors='coerce')
        won['updated_at_dt'] = pd.to_datetime(won['updated_at'], errors='coerce')
        won['duration_days'] = (won['updated_at_dt'] - won['created_at_dt']).dt.total_seconds() / 86400
        won = won.dropna(subset=['duration_days'])
        won = won[won['duration_days'] >= 0]

        # Filtrer les groupes vides
        won_filtered = won[won[group_col].notna() & (won[group_col] != '')]

        if won_filtered.empty:
            return {}

        result = {}
        for group, group_df in won_filtered.groupby(group_col):
            result[group] = round(group_df['duration_days'].mean(), 1)

        return result
    except Exception as e:
        logger.warning(f"Erreur calcul vélocité par {group_col}: {e}")
        return {}


def get_cold_deals(deals_df: pd.DataFrame, threshold_days: int = COLD_DEAL_THRESHOLD_DAYS) -> pd.DataFrame:
    """
    Identifie les deals "froids" : inactifs depuis plus de threshold_days
    et dont le statut n'est pas "Gagné".

    Returns:
        DataFrame avec colonne supplémentaire jours_inactifs
    """
    if deals_df.empty:
        return pd.DataFrame()

    df = deals_df.copy()

    # Exclure les deals gagnés
    df_active = df[~df['statut'].str.lower().str.strip().isin(WON_STATUSES)]

    if df_active.empty:
        return pd.DataFrame()

    try:
        now = datetime.now()
        df_active = df_active.copy()
        df_active['updated_at_dt'] = pd.to_datetime(df_active['updated_at'], errors='coerce')
        df_active = df_active.dropna(subset=['updated_at_dt'])

        threshold_date = now - timedelta(days=threshold_days)
        cold = df_active[df_active['updated_at_dt'] < threshold_date].copy()

        if cold.empty:
            return pd.DataFrame()

        cold['jours_inactifs'] = cold['updated_at_dt'].apply(
            lambda x: (now - x).days
        )
        cold = cold.sort_values('jours_inactifs', ascending=False)

        return cold
    except Exception as e:
        logger.warning(f"Erreur détection deals froids: {e}")
        return pd.DataFrame()
