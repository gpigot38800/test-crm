"""
Composants Streamlit pour l'affichage des KPIs.
Affiche le pipeline pondéré total et autres métriques clés.
"""

import streamlit as st
import pandas as pd
from business_logic.calculators import calculate_total_pipeline
from utils.formatters import format_currency


def display_pipeline_kpi(deals_df: pd.DataFrame):
    """
    Affiche le KPI "Pipeline Pondéré Total" avec st.metric().

    Args:
        deals_df: DataFrame contenant les deals avec colonne valeur_ponderee
    """
    # Calculer le pipeline total
    total_pipeline = calculate_total_pipeline(deals_df)

    # Afficher le metric
    st.metric(
        label="💰 Pipeline Pondéré Total",
        value=format_currency(total_pipeline),
        help="Somme des valeurs pondérées (montant × probabilité). "
             "Prévision du CA réel basée sur les probabilités de conversion par statut."
    )


def display_kpi_cards(deals_df: pd.DataFrame):
    """
    Affiche une série de KPI cards (pipeline, panier moyen, nombre deals, etc.).

    Args:
        deals_df: DataFrame contenant les deals
    """
    # Créer 4 colonnes pour les KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        display_pipeline_kpi(deals_df)

    with col2:
        _display_average_basket(deals_df)

    with col3:
        _display_total_deals(deals_df)

    with col4:
        _display_won_deals(deals_df)


def _display_average_basket(deals_df: pd.DataFrame):
    """Affiche le panier moyen (montant brut moyen)"""
    if deals_df.empty:
        avg_basket = 0
    else:
        avg_basket = deals_df['montant_brut'].mean()

    st.metric(
        label="🛒 Panier Moyen",
        value=format_currency(avg_basket),
        help="Montant moyen des deals (montant brut)"
    )


def _display_total_deals(deals_df: pd.DataFrame):
    """Affiche le nombre total de deals"""
    total_deals = len(deals_df)

    st.metric(
        label="📊 Nombre de Deals",
        value=f"{total_deals}",
        help="Nombre total de deals dans le pipeline"
    )


def _display_won_deals(deals_df: pd.DataFrame):
    """Affiche le nombre et pourcentage de deals gagnés"""
    if deals_df.empty:
        won_count = 0
        won_percent = 0
    else:
        won_count = len(deals_df[deals_df['statut'].str.lower() == 'gagné'])
        won_percent = (won_count / len(deals_df)) * 100

    st.metric(
        label="🏆 Deals Gagnés",
        value=f"{won_count}",
        delta=f"{won_percent:.1f}%",
        help="Nombre de deals gagnés et pourcentage du total"
    )
