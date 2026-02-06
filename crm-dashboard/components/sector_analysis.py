"""
Composant Streamlit pour l'analyse par secteur.
Affiche un graphique en barres montrant le montant total par secteur et identifie
les secteurs à haut panier moyen.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.formatters import format_currency


def display_sector_analysis(deals_df: pd.DataFrame):
    """
    Affiche l'analyse par secteur avec graphiques Plotly.

    Args:
        deals_df: DataFrame contenant les deals avec colonne secteur et montant_brut
    """
    st.subheader("🏢 Analyse par Secteur")

    # Vérifier si la colonne secteur existe et contient des données
    if deals_df.empty or 'secteur' not in deals_df.columns:
        st.info("Aucune donnée de secteur disponible.")
        return

    # Filtrer les deals sans secteur
    df_with_sector = deals_df[deals_df['secteur'].notna() & (deals_df['secteur'] != '')]

    if df_with_sector.empty:
        st.info("Aucun deal n'a de secteur assigné.")
        return

    # Créer deux colonnes pour les graphiques
    col1, col2 = st.columns(2)

    with col1:
        _display_sector_total_chart(df_with_sector)

    with col2:
        _display_sector_avg_basket_chart(df_with_sector)

    # Afficher le tableau récapitulatif
    st.markdown("---")
    _display_sector_summary_table(df_with_sector)


def _display_sector_total_chart(df: pd.DataFrame):
    """
    Affiche un graphique en barres horizontales du montant total par secteur.

    Args:
        df: DataFrame contenant les deals filtrés avec secteur
    """
    st.markdown("##### 💰 Montant Total par Secteur")

    # Grouper par secteur et calculer le total
    sector_totals = df.groupby('secteur')['montant_brut'].sum().sort_values(ascending=True)

    # Créer le graphique en barres horizontales
    fig = go.Figure(data=[
        go.Bar(
            x=sector_totals.values,
            y=sector_totals.index,
            orientation='h',
            marker=dict(
                color=sector_totals.values,
                colorscale='Blues',
                showscale=False
            ),
            text=[format_currency(val) for val in sector_totals.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Total: %{text}<extra></extra>'
        )
    ])

    fig.update_layout(
        xaxis_title="Montant Total (€)",
        yaxis_title="",
        height=max(300, len(sector_totals) * 40),
        margin=dict(l=20, r=100, t=20, b=20),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True
        )
    )

    st.plotly_chart(fig, width='stretch')

    # Afficher le secteur leader
    top_sector = sector_totals.index[-1]
    top_amount = sector_totals.values[-1]
    st.success(f"🏆 **Secteur leader** : {top_sector} avec {format_currency(top_amount)}")


def _display_sector_avg_basket_chart(df: pd.DataFrame):
    """
    Affiche un graphique en barres du panier moyen par secteur (Top 5).

    Args:
        df: DataFrame contenant les deals filtrés avec secteur
    """
    st.markdown("##### 🛒 Top 5 Secteurs - Panier Moyen")

    # Grouper par secteur et calculer la moyenne
    sector_avg = df.groupby('secteur')['montant_brut'].mean().sort_values(ascending=False).head(5)

    # Inverser pour affichage du plus petit au plus grand
    sector_avg_sorted = sector_avg.sort_values(ascending=True)

    # Créer le graphique en barres horizontales
    fig = go.Figure(data=[
        go.Bar(
            x=sector_avg_sorted.values,
            y=sector_avg_sorted.index,
            orientation='h',
            marker=dict(
                color=sector_avg_sorted.values,
                colorscale='Greens',
                showscale=False
            ),
            text=[format_currency(val) for val in sector_avg_sorted.values],
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Panier moyen: %{text}<extra></extra>'
        )
    ])

    fig.update_layout(
        xaxis_title="Panier Moyen (€)",
        yaxis_title="",
        height=max(300, len(sector_avg_sorted) * 40),
        margin=dict(l=20, r=100, t=20, b=20),
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True
        )
    )

    st.plotly_chart(fig, width='stretch')

    # Afficher le secteur avec le meilleur panier moyen
    best_sector = sector_avg.index[0]
    best_avg = sector_avg.values[0]
    st.success(f"💎 **Meilleur panier moyen** : {best_sector} avec {format_currency(best_avg)}")


def _display_sector_summary_table(df: pd.DataFrame):
    """
    Affiche un tableau récapitulatif avec toutes les métriques par secteur.

    Args:
        df: DataFrame contenant les deals filtrés avec secteur
    """
    st.markdown("##### 📊 Tableau Récapitulatif par Secteur")

    # Calculer les métriques par secteur
    summary = df.groupby('secteur').agg({
        'montant_brut': ['sum', 'mean', 'count'],
        'valeur_ponderee': 'sum'
    }).round(2)

    # Aplatir les colonnes multi-niveau
    summary.columns = ['Montant Total', 'Panier Moyen', 'Nombre Deals', 'Valeur Pondérée']

    # Trier par montant total décroissant
    summary = summary.sort_values('Montant Total', ascending=False)

    # Réinitialiser l'index pour afficher le secteur comme colonne
    summary = summary.reset_index()
    summary.columns = ['Secteur', 'Montant Total (€)', 'Panier Moyen (€)', 'Nombre Deals', 'Valeur Pondérée (€)']

    # Afficher le tableau avec formatage
    st.dataframe(
        summary,
        width='stretch',
        hide_index=True,
        column_config={
            'Secteur': st.column_config.TextColumn('Secteur', width='medium'),
            'Montant Total (€)': st.column_config.NumberColumn(
                'Montant Total',
                format='%.2f €',
                width='small'
            ),
            'Panier Moyen (€)': st.column_config.NumberColumn(
                'Panier Moyen',
                format='%.2f €',
                width='small'
            ),
            'Nombre Deals': st.column_config.NumberColumn(
                'Nb Deals',
                format='%d',
                width='small'
            ),
            'Valeur Pondérée (€)': st.column_config.NumberColumn(
                'Valeur Pondérée',
                format='%.2f €',
                width='small',
                help='Montant pondéré par les probabilités de conversion'
            )
        }
    )

    # Statistiques globales
    col1, col2, col3 = st.columns(3)

    with col1:
        total_sectors = len(summary)
        st.metric("🏢 Nombre de Secteurs", total_sectors)

    with col2:
        total_amount = summary['Montant Total (€)'].sum()
        st.metric("💰 Total Global", format_currency(total_amount))

    with col3:
        overall_avg = df['montant_brut'].mean()
        st.metric("🛒 Panier Moyen Global", format_currency(overall_avg))
