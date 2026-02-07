"""
Composant Streamlit pour la gestion des échéances.
Affiche les deals avec échéances dépassées (alertes rouges) et les deals à venir
dans les 30 prochains jours.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.formatters import format_currency


def display_deadline_management(deals_df: pd.DataFrame):
    """
    Affiche la gestion des échéances avec alertes pour dates dépassées
    et vue des 30 prochains jours.

    Args:
        deals_df: DataFrame contenant les deals avec colonne date_echeance
    """
    st.subheader("⏰ Gestion des Échéances")

    # Vérifier si la colonne date_echeance existe
    if deals_df.empty or 'date_echeance' not in deals_df.columns:
        st.info("Aucune donnée d'échéance disponible.")
        return

    # Filtrer les deals avec dates d'échéance
    df_with_deadline = deals_df[deals_df['date_echeance'].notna()].copy()

    if df_with_deadline.empty:
        st.info("Aucun deal n'a de date d'échéance assignée.")
        return

    # Convertir en datetime si nécessaire
    if not pd.api.types.is_datetime64_any_dtype(df_with_deadline['date_echeance']):
        df_with_deadline['date_echeance'] = pd.to_datetime(df_with_deadline['date_echeance'], errors='coerce')

    # Supprimer les dates invalides
    df_with_deadline = df_with_deadline[df_with_deadline['date_echeance'].notna()]

    if df_with_deadline.empty:
        st.info("Aucune date d'échéance valide trouvée.")
        return

    # Date actuelle
    today = pd.Timestamp.now().normalize()
    date_30_days = today + timedelta(days=30)

    # Séparer les deals selon leur statut d'échéance
    overdue_deals = df_with_deadline[df_with_deadline['date_echeance'] < today]
    upcoming_deals = df_with_deadline[
        (df_with_deadline['date_echeance'] >= today) &
        (df_with_deadline['date_echeance'] <= date_30_days)
    ]

    # Afficher les statistiques en haut
    _display_deadline_stats(overdue_deals, upcoming_deals, df_with_deadline)

    st.markdown("---")

    # Créer deux colonnes pour les deux listes
    col1, col2 = st.columns(2)

    with col1:
        _display_overdue_deals(overdue_deals)

    with col2:
        _display_upcoming_deals(upcoming_deals)


def _display_deadline_stats(overdue_df: pd.DataFrame, upcoming_df: pd.DataFrame, total_df: pd.DataFrame):
    """
    Affiche les statistiques des échéances.

    Args:
        overdue_df: DataFrame des deals en retard
        upcoming_df: DataFrame des deals à venir
        total_df: DataFrame de tous les deals avec échéances
    """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🚨 Échéances Dépassées",
            value=len(overdue_df),
            delta=f"-{len(overdue_df)} deals" if len(overdue_df) > 0 else "Aucun retard",
            delta_color="inverse" if len(overdue_df) > 0 else "off",
            help="Nombre de deals dont la date d'échéance est dépassée"
        )

    with col2:
        st.metric(
            label="📅 À Venir (30j)",
            value=len(upcoming_df),
            help="Nombre de deals avec échéance dans les 30 prochains jours"
        )

    with col3:
        # Calculer le montant total des deals à venir
        upcoming_amount = upcoming_df['montant_brut'].sum() if not upcoming_df.empty else 0
        st.metric(
            label="💰 CA Prévu (30j)",
            value=format_currency(upcoming_amount),
            help="Montant brut total des deals à venir dans les 30 jours"
        )

    with col4:
        # Pourcentage de deals avec échéance
        total_deals = len(total_df)
        pct_with_deadline = (total_deals / len(total_df.index)) * 100 if len(total_df.index) > 0 else 0
        st.metric(
            label="📊 Suivi Échéances",
            value=f"{pct_with_deadline:.0f}%",
            help="Pourcentage de deals avec date d'échéance définie"
        )


def _display_overdue_deals(overdue_df: pd.DataFrame):
    """
    Affiche la liste des deals avec échéances dépassées (en rouge).

    Args:
        overdue_df: DataFrame des deals en retard
    """
    st.markdown("##### 🚨 Échéances Dépassées")

    if overdue_df.empty:
        st.success("✅ Aucune échéance dépassée ! Excellent travail.")
        return

    # Trier par date croissante (les plus anciens en premier)
    overdue_sorted = overdue_df.sort_values('date_echeance', ascending=True)

    # Calculer le nombre de jours de retard
    today = pd.Timestamp.now().normalize()
    overdue_sorted['jours_retard'] = (today - overdue_sorted['date_echeance']).dt.days

    # Afficher un warning avec le nombre total
    st.error(f"⚠️ **{len(overdue_sorted)} deal(s) en retard**")

    # Afficher le tableau
    st.dataframe(
        overdue_sorted[[
            'client', 'statut', 'montant_brut', 'date_echeance',
            'jours_retard', 'secteur', 'assignee'
        ]],
        width='stretch',
        hide_index=True,
        column_config={
            'client': st.column_config.TextColumn('Client', width='medium'),
            'statut': st.column_config.TextColumn('Statut', width='small'),
            'montant_brut': st.column_config.NumberColumn(
                'Montant',
                format='%.2f €',
                width='small'
            ),
            'date_echeance': st.column_config.DateColumn(
                'Échéance',
                format='DD/MM/YYYY',
                width='small'
            ),
            'jours_retard': st.column_config.NumberColumn(
                '⏰ Retard',
                format='%d jours',
                width='small',
                help='Nombre de jours de retard'
            ),
            'secteur': st.column_config.TextColumn('Secteur', width='small'),
            'assignee': st.column_config.TextColumn('Commercial', width='small')
        }
    )

    # Afficher le deal le plus urgent
    most_urgent = overdue_sorted.iloc[0]
    st.warning(
        f"⚠️ **Plus urgent** : {most_urgent['client']} - "
        f"{most_urgent['jours_retard']} jours de retard "
        f"({format_currency(most_urgent['montant_brut'])})"
    )


def _display_upcoming_deals(upcoming_df: pd.DataFrame):
    """
    Affiche la liste des deals à venir dans les 30 prochains jours.

    Args:
        upcoming_df: DataFrame des deals à venir
    """
    st.markdown("##### 📅 Échéances à Venir (30 Jours)")

    if upcoming_df.empty:
        st.info("Aucune échéance prévue dans les 30 prochains jours.")
        return

    # Trier par date croissante (les plus proches en premier)
    upcoming_sorted = upcoming_df.sort_values('date_echeance', ascending=True)

    # Calculer le nombre de jours restants
    today = pd.Timestamp.now().normalize()
    upcoming_sorted['jours_restants'] = (upcoming_sorted['date_echeance'] - today).dt.days

    # Afficher un message informatif
    st.info(f"📊 **{len(upcoming_sorted)} deal(s) à clôturer dans les 30 jours**")

    # Afficher le tableau
    st.dataframe(
        upcoming_sorted[[
            'client', 'statut', 'montant_brut', 'date_echeance',
            'jours_restants', 'secteur', 'assignee'
        ]],
        width='stretch',
        hide_index=True,
        column_config={
            'client': st.column_config.TextColumn('Client', width='medium'),
            'statut': st.column_config.TextColumn('Statut', width='small'),
            'montant_brut': st.column_config.NumberColumn(
                'Montant',
                format='%.2f €',
                width='small'
            ),
            'date_echeance': st.column_config.DateColumn(
                'Échéance',
                format='DD/MM/YYYY',
                width='small'
            ),
            'jours_restants': st.column_config.NumberColumn(
                '⏳ Jours',
                format='%d j',
                width='small',
                help='Nombre de jours restants'
            ),
            'secteur': st.column_config.TextColumn('Secteur', width='small'),
            'assignee': st.column_config.TextColumn('Commercial', width='small')
        }
    )

    # Afficher le prochain deal à clôturer
    next_deal = upcoming_sorted.iloc[0]

    # Déterminer la couleur du message selon la proximité
    if next_deal['jours_restants'] <= 7:
        st.warning(
            f"⏰ **Cette semaine** : {next_deal['client']} - "
            f"J-{next_deal['jours_restants']} "
            f"({format_currency(next_deal['montant_brut'])})"
        )
    else:
        st.success(
            f"🎯 **Prochain deal** : {next_deal['client']} - "
            f"J-{next_deal['jours_restants']} "
            f"({format_currency(next_deal['montant_brut'])})"
        )
