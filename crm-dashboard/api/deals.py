"""
Blueprint API pour la gestion des deals.
Expose les endpoints CRUD pour les deals.
"""

from flask import Blueprint, jsonify, request
from database.crud import (
    get_all_deals, get_filtered_deals, get_deal_by_id,
    insert_deal, update_deal, delete_deal, clear_all_deals
)
from business_logic.validators import validate_deal_dict, parse_date
from business_logic.calculators import calculate_probability, calculate_weighted_value

deals_bp = Blueprint('deals', __name__)


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


@deals_bp.route('/deals', methods=['GET'])
def get_deals():
    """GET /api/deals - Retourne tous les deals (avec filtres optionnels)"""
    try:
        params = _extract_filter_params()
        if params:
            df = get_filtered_deals(params)
        else:
            df = get_all_deals()
        deals = df.to_dict(orient='records')
        return jsonify({"success": True, "data": deals, "error": None})
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@deals_bp.route('/deals', methods=['POST'])
def create_deal():
    """POST /api/deals - Crée un nouveau deal"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "data": None, "error": "Corps JSON requis"}), 400

        # Validation
        is_valid, errors = validate_deal_dict(data)
        if not is_valid:
            return jsonify({"success": False, "data": None, "error": "; ".join(errors)}), 400

        # Calcul probabilité et valeur pondérée
        statut = str(data.get('statut', '')).strip()
        probabilite = calculate_probability(statut)
        montant_brut = float(data['montant_brut'])
        valeur_ponderee = calculate_weighted_value(montant_brut, probabilite)

        # Préparer le dict pour insertion
        deal_dict = {
            "client": str(data['client']).strip(),
            "statut": statut,
            "montant_brut": montant_brut,
            "probabilite": probabilite,
            "valeur_ponderee": valeur_ponderee,
            "secteur": str(data.get('secteur', '')).strip() or None,
            "date_echeance": parse_date(str(data.get('date_echeance', ''))) if data.get('date_echeance') else None,
            "assignee": str(data.get('assignee', '')).strip() or None,
            "notes": str(data.get('notes', '')).strip() or None
        }

        created = insert_deal(deal_dict)
        return jsonify({"success": True, "data": created, "error": None}), 201

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@deals_bp.route('/deals/<int:deal_id>', methods=['PUT'])
def update_deal_endpoint(deal_id):
    """PUT /api/deals/<id> - Modifie un deal existant"""
    try:
        existing = get_deal_by_id(deal_id)
        if existing is None:
            return jsonify({"success": False, "data": None, "error": "Deal non trouvé"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"success": False, "data": None, "error": "Corps JSON requis"}), 400

        # Fusionner avec les données existantes pour validation complète
        merged = {**existing, **data}
        is_valid, errors = validate_deal_dict(merged)
        if not is_valid:
            return jsonify({"success": False, "data": None, "error": "; ".join(errors)}), 400

        # Recalculer probabilité et valeur pondérée
        statut = str(merged.get('statut', '')).strip()
        probabilite = calculate_probability(statut)
        montant_brut = float(merged['montant_brut'])
        valeur_ponderee = calculate_weighted_value(montant_brut, probabilite)

        # Préparer le dict pour mise à jour
        update_dict = {
            "client": str(merged['client']).strip(),
            "statut": statut,
            "montant_brut": montant_brut,
            "probabilite": probabilite,
            "valeur_ponderee": valeur_ponderee,
            "secteur": str(merged.get('secteur', '')).strip() or None,
            "date_echeance": parse_date(str(merged.get('date_echeance', ''))) if merged.get('date_echeance') else None,
            "assignee": str(merged.get('assignee', '')).strip() or None,
            "notes": str(merged.get('notes', '')).strip() or None
        }

        updated = update_deal(deal_id, update_dict)
        return jsonify({"success": True, "data": updated, "error": None})

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@deals_bp.route('/deals/<int:deal_id>', methods=['DELETE'])
def delete_deal_endpoint(deal_id):
    """DELETE /api/deals/<id> - Supprime un deal individuel"""
    try:
        deleted = delete_deal(deal_id)
        if not deleted:
            return jsonify({"success": False, "data": None, "error": "Deal non trouvé"}), 404
        return jsonify({"success": True, "data": {"message": "Deal supprimé"}, "error": None})
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500


@deals_bp.route('/deals', methods=['DELETE'])
def delete_deals():
    """DELETE /api/deals - Supprime tous les deals"""
    try:
        clear_all_deals()
        return jsonify({"success": True, "data": {"message": "Tous les deals ont été supprimés"}, "error": None})
    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500
