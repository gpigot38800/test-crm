"""
Dashboard CRM - Application principale Streamlit.
Point d'entrée de l'application: gère l'initialisation et l'orchestration des composants.
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Ajouter le répertoire parent au PYTHONPATH pour les imports
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import init_database
from database.crud import get_all_deals
from components.csv_uploader import display_csv_uploader
from components.kpi_cards import display_kpi_cards


def main():
    """Point d'entrée principal de l'application"""

    # Configuration de la page Streamlit
    st.set_page_config(
        page_title="Dashboard CRM",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialisation de la base de données
    try:
        init_database()
    except Exception as e:
        st.error(f"❌ Erreur lors de l'initialisation de la base de données: {str(e)}")
        st.stop()

    # Titre principal
    st.title("📊 Dashboard CRM - Fondateur")
    st.markdown("---")

    # Sidebar: CSV Uploader
    display_csv_uploader()

    # Bouton refresh dans sidebar
    if st.sidebar.button("🔄 Actualiser les données"):
        if 'deals_df' in st.session_state:
            del st.session_state['deals_df']
        st.rerun()

    # Charger les deals (avec cache session_state)
    deals_df = load_deals()

    # Vérifier si des données existent
    if deals_df.empty:
        st.info("👋 Bienvenue ! Commencez par importer un fichier CSV pour voir votre pipeline.")
        st.markdown("""
        ### 📝 Instructions

        1. Cliquez sur **"Choisir un fichier CSV"** dans la sidebar
        2. Sélectionnez votre fichier contenant les colonnes suivantes :
           - `Client` (requis)
           - `Statut` (requis): Prospect, Qualifié, Négociation, Gagné
           - `Montant` (requis)
           - `Tags` (optionnel): Secteur d'activité
           - `Date Échéance` (optionnel)
           - `Assignee` (optionnel): Commercial responsable
           - `Notes` (optionnel)
        3. Cliquez sur **"🚀 Importer le CSV"**
        4. Visualisez votre pipeline pondéré !
        """)
        st.stop()

    # Afficher les KPIs en haut de page
    st.subheader("📈 Indicateurs Clés")
    display_kpi_cards(deals_df)

    st.markdown("---")

    # Section: Aperçu des deals
    st.subheader("🗂️ Aperçu des Deals")

    # Afficher le DataFrame avec formatage
    st.dataframe(
        deals_df[[
            'client', 'statut', 'montant_brut', 'probabilite',
            'valeur_ponderee', 'secteur', 'date_echeance', 'assignee'
        ]],
        use_container_width=True,
        hide_index=True,
        column_config={
            'client': st.column_config.TextColumn('Client', width='medium'),
            'statut': st.column_config.TextColumn('Statut', width='small'),
            'montant_brut': st.column_config.NumberColumn(
                'Montant Brut',
                format='%.2f €',
                width='small'
            ),
            'probabilite': st.column_config.NumberColumn(
                'Probabilité',
                format='%.0f%%',
                width='small',
                help='Probabilité de conversion selon le statut'
            ),
            'valeur_ponderee': st.column_config.NumberColumn(
                'Valeur Pondérée',
                format='%.2f €',
                width='medium',
                help='Montant × Probabilité'
            ),
            'secteur': st.column_config.TextColumn('Secteur', width='small'),
            'date_echeance': st.column_config.DateColumn(
                'Date Échéance',
                format='DD/MM/YYYY',
                width='small'
            ),
            'assignee': st.column_config.TextColumn('Commercial', width='small')
        }
    )

    # Footer
    st.markdown("---")
    st.caption("Dashboard CRM MVP - Phase 1 | Import CSV & Pipeline Pondéré")


@st.cache_data(ttl=300)
def load_deals() -> pd.DataFrame:
    """
    Charge les deals depuis la base de données avec cache de 5 minutes.

    Returns:
        pd.DataFrame: DataFrame contenant tous les deals

    Note:
        Cache TTL = 300s (5 min) pour éviter requêtes excessives.
        Peut être invalidé manuellement via bouton refresh.
    """
    try:
        # Vérifier si données en session_state (refresh manuel)
        if 'deals_df' in st.session_state:
            return st.session_state['deals_df']

        # Charger depuis DB
        deals_df = get_all_deals()

        # Convertir probabilité en pourcentage pour affichage
        if not deals_df.empty and 'probabilite' in deals_df.columns:
            deals_df['probabilite'] = deals_df['probabilite'] * 100

        return deals_df

    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        return pd.DataFrame()


if __name__ == "__main__":
    main()
