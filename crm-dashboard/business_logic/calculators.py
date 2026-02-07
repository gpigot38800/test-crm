"""
Fonctions de calcul métier.
Calcule les probabilités, valeurs pondérées et le pipeline total.
"""

import pandas as pd
from typing import Union, List, Dict, Any
import logging
from utils.constants import PROBABILITY_MAP

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
