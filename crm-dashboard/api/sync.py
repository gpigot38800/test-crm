"""
Blueprint Flask pour la synchronisation avec services externes (Airtable, Notion).
Endpoints : configuration des connecteurs, test de connexion, import/export, logs.
"""

import json
import logging
from datetime import datetime

from flask import Blueprint, request, jsonify

from database.crud import (
    get_connector_config, get_all_connector_configs, upsert_connector_config,
    insert_sync_log, get_sync_logs,
    get_all_deals, get_deal_by_client, insert_deal, update_deal
)
from connectors.airtable import AirtableConnector
from connectors.notion import NotionConnector
from connectors.field_mapping import get_field_mapping, normalize_status
from business_logic.calculators import calculate_probability, calculate_weighted_value

logger = logging.getLogger(__name__)

sync_bp = Blueprint('sync', __name__)

VALID_PROVIDERS = ['airtable', 'notion']


def _get_connector(provider: str, config: dict):
    """Instancie le connecteur approprié selon le provider."""
    if provider == 'airtable':
        return AirtableConnector(config)
    elif provider == 'notion':
        return NotionConnector(config)
    return None


# --- Configuration endpoints ---

@sync_bp.route('/connectors/config', methods=['GET'])
def get_configs():
    """Retourne toutes les configurations de connecteurs (tokens masqués)."""
    try:
        configs = get_all_connector_configs()
        # Masquer les tokens
        for cfg in configs:
            if cfg.get('api_token'):
                cfg['api_token'] = '***'
        return jsonify({"success": True, "data": configs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@sync_bp.route('/connectors/config/<provider>', methods=['PUT'])
def save_config(provider):
    """Sauvegarde la configuration d'un connecteur."""
    if provider not in VALID_PROVIDERS:
        return jsonify({
            "success": False,
            "error": f"Provider non supporté. Valeurs acceptées: {', '.join(VALID_PROVIDERS)}"
        }), 400

    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Corps JSON requis"}), 400

        # Préparer les données à sauvegarder
        config_data = {}

        if 'api_token' in data and data['api_token'] != '***':
            config_data['api_token'] = data['api_token']

        if 'base_id' in data:
            config_data['base_id'] = data['base_id']

        if 'table_name' in data:
            config_data['table_name'] = data['table_name']

        if 'field_mapping' in data:
            mapping = data['field_mapping']
            config_data['field_mapping'] = json.dumps(mapping) if isinstance(mapping, dict) else mapping

        if 'is_active' in data:
            config_data['is_active'] = bool(data['is_active'])

        result = upsert_connector_config(provider, config_data)

        # Masquer le token dans la réponse
        if result and result.get('api_token'):
            result['api_token'] = '***'

        return jsonify({"success": True, "data": result})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# --- Test connection endpoint ---

@sync_bp.route('/connectors/test/<provider>', methods=['POST'])
def test_connection(provider):
    """Teste la connexion à un service externe."""
    if provider not in VALID_PROVIDERS:
        return jsonify({
            "success": False,
            "error": f"Provider non supporté. Valeurs acceptées: {', '.join(VALID_PROVIDERS)}"
        }), 400

    try:
        config = get_connector_config(provider)
        if not config:
            return jsonify({
                "success": False,
                "error": f"Aucune configuration trouvée pour {provider}. Configurez d'abord le connecteur."
            }), 400

        connector = _get_connector(provider, config)
        result = connector.test_connection()
        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# --- Import endpoint ---

@sync_bp.route('/sync/<provider>/import', methods=['POST'])
def sync_import(provider):
    """Importe les deals depuis un service externe vers le CRM."""
    if provider not in VALID_PROVIDERS:
        return jsonify({
            "success": False,
            "error": f"Provider non supporté. Valeurs acceptées: {', '.join(VALID_PROVIDERS)}"
        }), 400

    started_at = datetime.now().isoformat()

    try:
        config = get_connector_config(provider)
        if not config:
            return jsonify({
                "success": False,
                "error": f"Aucune configuration trouvée pour {provider}."
            }), 400

        connector = _get_connector(provider, config)
        field_mapping = get_field_mapping(config)

        # Récupérer les records depuis le service externe
        external_deals = connector.fetch_records(field_mapping)

        created = 0
        updated = 0
        errors = []
        unknown_statuses = []

        for ext_deal in external_deals:
            try:
                client_name = ext_deal.get('client')
                if not client_name:
                    errors.append("Record sans nom de client, ignoré")
                    continue

                montant_brut = ext_deal.get('montant_brut')
                if montant_brut is None or montant_brut <= 0:
                    errors.append(f"'{client_name}': montant_brut invalide ({montant_brut})")
                    continue

                # Normaliser le statut (anglais → français)
                raw_statut = ext_deal.get('statut', '')
                normalized_statut = normalize_status(raw_statut)
                if normalized_statut is None:
                    normalized_statut = 'prospect'
                    unknown_statuses.append(f"'{client_name}': statut '{raw_statut}' inconnu → prospect")

                # Calculer probabilité et valeur pondérée
                probabilite = calculate_probability(normalized_statut)
                valeur_ponderee = calculate_weighted_value(montant_brut, probabilite)

                deal_data = {
                    'client': client_name,
                    'statut': normalized_statut,
                    'montant_brut': montant_brut,
                    'probabilite': probabilite,
                    'valeur_ponderee': valeur_ponderee,
                    'secteur': ext_deal.get('secteur'),
                    'date_echeance': ext_deal.get('date_echeance'),
                    'assignee': ext_deal.get('assignee'),
                    'notes': ext_deal.get('notes'),
                }

                # Vérifier si le deal existe déjà (par client)
                existing = get_deal_by_client(client_name)

                if existing:
                    update_deal(existing['id'], deal_data)
                    updated += 1
                else:
                    insert_deal(deal_data)
                    created += 1

            except Exception as e:
                errors.append(f"'{ext_deal.get('client', '?')}': {str(e)}")

        # Déterminer le statut global
        total_processed = created + updated + len(errors)
        if errors and (created + updated) > 0:
            sync_status = 'partial'
        elif errors:
            sync_status = 'error'
        else:
            sync_status = 'success'

        # Logger la synchronisation
        completed_at = datetime.now().isoformat()
        error_msg = '; '.join(errors + unknown_statuses) if (errors or unknown_statuses) else None
        insert_sync_log({
            'provider': provider,
            'direction': 'import',
            'status': sync_status,
            'records_processed': total_processed,
            'records_created': created,
            'records_updated': updated,
            'error_message': error_msg,
            'started_at': started_at,
            'completed_at': completed_at
        })

        return jsonify({
            "success": True,
            "status": sync_status,
            "records_processed": total_processed,
            "records_created": created,
            "records_updated": updated,
            "errors": errors,
            "unknown_statuses": unknown_statuses
        })

    except Exception as e:
        # Logger l'erreur
        insert_sync_log({
            'provider': provider,
            'direction': 'import',
            'status': 'error',
            'records_processed': 0,
            'records_created': 0,
            'records_updated': 0,
            'error_message': str(e),
            'started_at': started_at,
            'completed_at': datetime.now().isoformat()
        })
        return jsonify({"success": False, "error": str(e)}), 500


# --- Export endpoint ---

@sync_bp.route('/sync/<provider>/export', methods=['POST'])
def sync_export(provider):
    """Exporte les deals du CRM vers un service externe."""
    if provider not in VALID_PROVIDERS:
        return jsonify({
            "success": False,
            "error": f"Provider non supporté. Valeurs acceptées: {', '.join(VALID_PROVIDERS)}"
        }), 400

    started_at = datetime.now().isoformat()

    try:
        config = get_connector_config(provider)
        if not config:
            return jsonify({
                "success": False,
                "error": f"Aucune configuration trouvée pour {provider}."
            }), 400

        connector = _get_connector(provider, config)
        field_mapping = get_field_mapping(config)

        # Récupérer tous les deals du CRM
        deals_df = get_all_deals()

        if deals_df.empty:
            insert_sync_log({
                'provider': provider,
                'direction': 'export',
                'status': 'success',
                'records_processed': 0,
                'records_created': 0,
                'records_updated': 0,
                'error_message': None,
                'started_at': started_at,
                'completed_at': datetime.now().isoformat()
            })
            return jsonify({
                "success": True,
                "status": "success",
                "records_processed": 0,
                "records_created": 0,
                "records_updated": 0,
                "message": "Aucun deal à exporter"
            })

        deals_list = deals_df.to_dict('records')
        result = connector.push_records(deals_list, field_mapping)

        total = result['records_created'] + result['records_updated'] + len(result.get('errors', []))
        sync_status = 'partial' if result.get('errors') else 'success'

        completed_at = datetime.now().isoformat()
        error_msg = '; '.join(result.get('errors', [])) if result.get('errors') else None
        insert_sync_log({
            'provider': provider,
            'direction': 'export',
            'status': sync_status,
            'records_processed': total,
            'records_created': result['records_created'],
            'records_updated': result['records_updated'],
            'error_message': error_msg,
            'started_at': started_at,
            'completed_at': completed_at
        })

        return jsonify({
            "success": True,
            "status": sync_status,
            "records_processed": total,
            "records_created": result['records_created'],
            "records_updated": result['records_updated'],
            "errors": result.get('errors', [])
        })

    except Exception as e:
        insert_sync_log({
            'provider': provider,
            'direction': 'export',
            'status': 'error',
            'records_processed': 0,
            'records_created': 0,
            'records_updated': 0,
            'error_message': str(e),
            'started_at': started_at,
            'completed_at': datetime.now().isoformat()
        })
        return jsonify({"success": False, "error": str(e)}), 500


# --- Sync logs endpoint ---

@sync_bp.route('/sync/logs', methods=['GET'])
def get_logs():
    """Retourne l'historique des synchronisations."""
    try:
        provider_filter = request.args.get('provider')
        limit = request.args.get('limit', 50, type=int)

        logs = get_sync_logs(limit=limit, provider_filter=provider_filter)
        return jsonify({"success": True, "data": logs})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
