"""
Blueprint API pour la gestion des deals.
Expose les endpoints GET /api/deals et DELETE /api/deals.
"""

from flask import Blueprint, jsonify
from database.crud import get_all_deals, clear_all_deals

deals_bp = Blueprint('deals', __name__)


@deals_bp.route('/deals', methods=['GET'])
def get_deals():
    """GET /api/deals - Retourne tous les deals"""
    try:
        df = get_all_deals()
        deals = df.to_dict(orient='records')
        return jsonify({"success": True, "data": deals, "error": None})
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
