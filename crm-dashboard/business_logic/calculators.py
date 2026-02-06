"""
Fonctions de calcul métier.
Calcule les probabilités, valeurs pondérées et le pipeline total.
"""

import pandas as pd
from typing import Union
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
