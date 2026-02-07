"""
Blueprint API pour les analytics (KPIs, secteurs, échéances, performance).
Expose les endpoints GET /api/kpis, GET /api/analytics/sectors,
GET /api/analytics/deadlines, GET /api/analytics/performance, GET /api/filters/options.
"""

from flask import Blueprint, jsonify, request
from database.crud import get_all_deals, get_filtered_deals, get_filter_options
from business_logic.calculators import calculate_total_pipeline, calculate_performance_by_assignee
from utils.formatters import format_currency
from datetime import datetime, timedelta
import pandas as pd

analytics_bp = Blueprint('analytics', __name__)


def _extract_filter_params():
    """Extrait les paramètres de filtrage depuis request.args."""
    params = {}
    if request.args.get('statut'):
        params['statut'] = request.args.getlist('statut')
    if request.args.get('secteur'):
        params['secteur'] = request.args.getlist('secteur')
    if request.args.get('assignee'):
        params['assignee'] = request.args.getlist('assignee')
    if request.args.get('date_from'):
        params['date_from'] = request.args.get('date_from')
    if request.args.get('date_to'):
        params['date_to'] = request.args.get('date_to')
    if request.args.get('search'):
        params['search'] = request.args.get('search')
    return params


def _get_deals():
    """Récupère les deals en appliquant les filtres si présents."""
    params = _extract_filter_params()
    if params:
        return get_filtered_deals(params)
    return get_all_deals()


@analytics_bp.route('/kpis', methods=['GET'])
def get_kpis():
    """GET /api/kpis - Retourne les KPIs calculés (avec filtres optionnels)"""
    try:
        df = _get_deals()

        if df.empty:
            return jsonify({"success": True, "data": {
                "pipeline_pondere": 0,
                "pipeline_pondere_formatted": "0 €",
                "panier_moyen": 0,
                "panier_moyen_formatted": "0 €",
                "nombre_deals": 0,
                "deals_gagnes": 0,
                "taux_conversion": 0
            }, "error": None})

        pipeline = calculate_total_pipeline(df)
        panier_moyen = round(df['montant_brut'].mean(), 2)
        nombre_deals = len(df)
        deals_gagnes = len(df[df['statut'].str.lower().str.strip().isin(['gagné', 'gagné - en cours'])])
        taux_conversion = round((deals_gagnes / nombre_deals) * 100, 1) if nombre_deals > 0 else 0

        return jsonify({"success": True, "data": {
            "pipeline_pondere": pipeline,
            "pipeline_pondere_formatted": format_currency(pipeline),
            "panier_moyen": panier_moyen,
            "panier_moyen_formatted": format_currency(panier_moyen),
            "nombre_deals": nombre_deals,
            "deals_gagnes": deals_gagnes,
            "taux_conversion": taux_conversion
        }, "error": None})

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@analytics_bp.route('/analytics/sectors', methods=['GET'])
def get_sectors():
    """GET /api/analytics/sectors - Analyse par secteur (avec filtres optionnels)"""
    try:
        df = _get_deals()

        if df.empty:
            return jsonify({"success": True, "data": {
                "chart_montants": {"labels": [], "datasets": [{"data": []}]},
                "chart_panier_moyen": {"labels": [], "datasets": [{"data": []}]},
                "tableau": []
            }, "error": None})

        # Filtrer les deals sans secteur
        df_sectors = df[df['secteur'].notna() & (df['secteur'] != '')]

        if df_sectors.empty:
            return jsonify({"success": True, "data": {
                "chart_montants": {"labels": [], "datasets": [{"data": []}]},
                "chart_panier_moyen": {"labels": [], "datasets": [{"data": []}]},
                "tableau": []
            }, "error": None})

        # Montants totaux par secteur
        montants = df_sectors.groupby('secteur')['montant_brut'].sum().sort_values(ascending=True)

        # Paniers moyens par secteur
        paniers = df_sectors.groupby('secteur')['montant_brut'].mean()

        # Top 5 paniers moyens
        top5_paniers = paniers.sort_values(ascending=False).head(5).sort_values(ascending=True)

        # Nombre de deals par secteur
        nb_deals = df_sectors.groupby('secteur').size()

        # Valeur pondérée par secteur
        valeur_ponderee = df_sectors.groupby('secteur')['valeur_ponderee'].sum()

        # Tableau récapitulatif
        tableau = []
        for secteur in montants.sort_values(ascending=False).index:
            tableau.append({
                "secteur": secteur,
                "montant_total": round(montants[secteur], 2),
                "montant_total_formatted": format_currency(montants[secteur]),
                "panier_moyen": round(paniers[secteur], 2),
                "panier_moyen_formatted": format_currency(paniers[secteur]),
                "nb_deals": int(nb_deals[secteur]),
                "valeur_ponderee": round(valeur_ponderee[secteur], 2),
                "valeur_ponderee_formatted": format_currency(valeur_ponderee[secteur])
            })

        # Données Chart.js - Montants totaux
        chart_montants = {
            "labels": montants.index.tolist(),
            "datasets": [{
                "label": "Montant Total (€)",
                "data": [round(v, 2) for v in montants.values.tolist()],
                "backgroundColor": "rgba(59, 130, 246, 0.7)",
                "borderColor": "rgba(59, 130, 246, 1)",
                "borderWidth": 1
            }]
        }

        # Données Chart.js - Top 5 Paniers Moyens
        chart_panier_moyen = {
            "labels": top5_paniers.index.tolist(),
            "datasets": [{
                "label": "Panier Moyen (€)",
                "data": [round(v, 2) for v in top5_paniers.values.tolist()],
                "backgroundColor": "rgba(34, 197, 94, 0.7)",
                "borderColor": "rgba(34, 197, 94, 1)",
                "borderWidth": 1
            }]
        }

        return jsonify({"success": True, "data": {
            "chart_montants": chart_montants,
            "chart_panier_moyen": chart_panier_moyen,
            "tableau": tableau
        }, "error": None})

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@analytics_bp.route('/analytics/deadlines', methods=['GET'])
def get_deadlines():
    """GET /api/analytics/deadlines - Échéances dépassées et à venir (avec filtres optionnels)"""
    try:
        df = _get_deals()

        if df.empty:
            return jsonify({"success": True, "data": {
                "overdue": [], "upcoming": [],
                "stats": {"nb_overdue": 0, "nb_upcoming": 0, "montant_upcoming": 0}
            }, "error": None})

        today = datetime.now().date()
        in_30_days = today + timedelta(days=30)

        # Filtrer les deals avec date d'échéance
        df_dated = df[df['date_echeance'].notna() & (df['date_echeance'] != '')].copy()

        if df_dated.empty:
            return jsonify({"success": True, "data": {
                "overdue": [], "upcoming": [],
                "stats": {"nb_overdue": 0, "nb_upcoming": 0, "montant_upcoming": 0}
            }, "error": None})

        df_dated['date_parsed'] = pd.to_datetime(df_dated['date_echeance'], errors='coerce').dt.date
        df_dated = df_dated.dropna(subset=['date_parsed'])

        # Deals en retard
        overdue_df = df_dated[df_dated['date_parsed'] < today].sort_values('date_parsed')
        overdue = []
        for _, row in overdue_df.iterrows():
            jours_retard = (today - row['date_parsed']).days
            overdue.append({
                "client": row['client'],
                "statut": row['statut'],
                "montant_brut": row['montant_brut'],
                "montant_formatted": format_currency(row['montant_brut']),
                "date_echeance": row['date_echeance'],
                "jours_retard": jours_retard,
                "secteur": row.get('secteur', ''),
                "assignee": row.get('assignee', '')
            })

        # Deals à venir (30 jours)
        upcoming_df = df_dated[(df_dated['date_parsed'] >= today) & (df_dated['date_parsed'] <= in_30_days)].sort_values('date_parsed')
        upcoming = []
        for _, row in upcoming_df.iterrows():
            jours_restants = (row['date_parsed'] - today).days
            upcoming.append({
                "client": row['client'],
                "statut": row['statut'],
                "montant_brut": row['montant_brut'],
                "montant_formatted": format_currency(row['montant_brut']),
                "date_echeance": row['date_echeance'],
                "jours_restants": jours_restants,
                "secteur": row.get('secteur', ''),
                "assignee": row.get('assignee', '')
            })

        montant_upcoming = sum(d['montant_brut'] for d in upcoming)

        return jsonify({"success": True, "data": {
            "overdue": overdue,
            "upcoming": upcoming,
            "stats": {
                "nb_overdue": len(overdue),
                "nb_upcoming": len(upcoming),
                "montant_upcoming": round(montant_upcoming, 2),
                "montant_upcoming_formatted": format_currency(montant_upcoming)
            }
        }, "error": None})

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@analytics_bp.route('/analytics/performance', methods=['GET'])
def get_performance():
    """GET /api/analytics/performance - Performance par commercial (avec filtres optionnels)"""
    try:
        df = _get_deals()

        if df.empty:
            return jsonify({"success": True, "data": {
                "performance": [],
                "chart_data": {"labels": [], "datasets": []},
                "stats": {"nb_commerciaux": 0}
            }, "error": None})

        performance = calculate_performance_by_assignee(df)

        # Formater les montants
        for p in performance:
            p["montant_total_formatted"] = format_currency(p["montant_total"])
            p["pipeline_pondere_formatted"] = format_currency(p["pipeline_pondere"])
            p["panier_moyen_formatted"] = format_currency(p["panier_moyen"])

        # Données Chart.js
        labels = [p["assignee"] for p in performance]
        chart_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Nombre de Deals",
                    "data": [p["nb_deals"] for p in performance],
                    "backgroundColor": "rgba(59, 130, 246, 0.7)",
                    "borderColor": "rgba(59, 130, 246, 1)",
                    "borderWidth": 1,
                    "yAxisID": "y"
                },
                {
                    "label": "Taux de Conversion (%)",
                    "data": [p["taux_conversion"] for p in performance],
                    "backgroundColor": "rgba(34, 197, 94, 0.7)",
                    "borderColor": "rgba(34, 197, 94, 1)",
                    "borderWidth": 1,
                    "yAxisID": "y1"
                }
            ]
        }

        return jsonify({"success": True, "data": {
            "performance": performance,
            "chart_data": chart_data,
            "stats": {"nb_commerciaux": len(performance)}
        }, "error": None})

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@analytics_bp.route('/filters/options', methods=['GET'])
def get_filters_options():
    """GET /api/filters/options - Retourne les valeurs disponibles pour les filtres"""
    try:
        options = get_filter_options()
        return jsonify({"success": True, "data": options, "error": None})
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500
