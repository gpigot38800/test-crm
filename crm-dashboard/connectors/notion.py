"""
Connecteur Notion : synchronisation bidirectionnelle des deals via API REST.
Utilise requests directement (compatible Python 3.14).
"""

import logging
import time
from typing import Dict, List, Any, Optional

import requests

from .base import BaseConnector
from .field_mapping import convert_crm_to_external

logger = logging.getLogger(__name__)

NOTION_API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"


def _extract_notion_value(prop: Dict[str, Any]) -> Any:
    """Extrait une valeur Python depuis une propriété Notion."""
    if not prop:
        return None

    prop_type = prop.get('type', '')

    if prop_type == 'title':
        items = prop.get('title', [])
        return items[0]['text']['content'] if items else None

    if prop_type == 'rich_text':
        items = prop.get('rich_text', [])
        return items[0]['text']['content'] if items else None

    if prop_type == 'number':
        return prop.get('number')

    if prop_type == 'date':
        date_obj = prop.get('date')
        return date_obj.get('start') if date_obj else None

    if prop_type == 'select':
        select_obj = prop.get('select')
        return select_obj.get('name') if select_obj else None

    if prop_type == 'status':
        status_obj = prop.get('status')
        return status_obj.get('name') if status_obj else None

    if prop_type == 'multi_select':
        items = prop.get('multi_select', [])
        return ', '.join([item['name'] for item in items]) if items else None

    if prop_type == 'checkbox':
        return prop.get('checkbox')

    return None


def _build_notion_property(crm_field: str, value: Any) -> Optional[Dict[str, Any]]:
    """Construit une propriété Notion depuis un champ CRM et sa valeur."""
    if value is None:
        return None

    if crm_field == 'client':
        return {"title": [{"text": {"content": str(value)}}]}

    if crm_field in ('notes', 'secteur', 'assignee'):
        return {"rich_text": [{"text": {"content": str(value)}}]}

    if crm_field == 'montant_brut':
        try:
            return {"number": float(value)}
        except (ValueError, TypeError):
            return None

    if crm_field == 'date_echeance':
        return {"date": {"start": str(value)}}

    if crm_field == 'statut':
        return {"select": {"name": str(value)}}

    return {"rich_text": [{"text": {"content": str(value)}}]}


class NotionConnector(BaseConnector):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.database_id = self.base_id

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION
        }

    def _query_all_pages(self) -> List[Dict]:
        """Récupère toutes les pages avec pagination."""
        pages = []
        start_cursor = None
        while True:
            body = {}
            if start_cursor:
                body['start_cursor'] = start_cursor

            resp = requests.post(
                f"{NOTION_API_BASE}/databases/{self.database_id}/query",
                headers=self._headers(),
                json=body
            )
            resp.raise_for_status()
            data = resp.json()
            pages.extend(data.get('results', []))

            if not data.get('has_more', False):
                break
            start_cursor = data.get('next_cursor')
        return pages

    def test_connection(self) -> Dict[str, Any]:
        try:
            # Récupérer les infos de la database
            resp = requests.get(
                f"{NOTION_API_BASE}/databases/{self.database_id}",
                headers=self._headers()
            )
            resp.raise_for_status()
            db = resp.json()

            title_parts = db.get('title', [])
            db_title = title_parts[0]['plain_text'] if title_parts else 'Sans titre'

            pages = self._query_all_pages()

            return {
                "success": True,
                "message": "Connexion Notion réussie",
                "table_name": db_title,
                "record_count": len(pages)
            }
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            if status == 401:
                return {"success": False, "message": "Token Notion invalide ou révoqué"}
            if status == 404:
                return {"success": False, "message": "Base de données Notion inaccessible. Vérifiez que l'intégration est connectée à la page."}
            return {"success": False, "message": f"Erreur Notion HTTP {status}"}
        except Exception as e:
            return {"success": False, "message": f"Erreur connexion Notion: {str(e)}"}

    def fetch_records(self, field_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
        all_pages = self._query_all_pages()

        deals = []
        for page in all_pages:
            properties = page.get('properties', {})
            deal = {}

            for crm_field, external_field in field_mapping.items():
                prop = properties.get(external_field)
                deal[crm_field] = _extract_notion_value(prop)

            if deal.get('montant_brut') is not None:
                try:
                    deal['montant_brut'] = float(deal['montant_brut'])
                except (ValueError, TypeError):
                    deal['montant_brut'] = None

            deal['_notion_page_id'] = page.get('id')
            deals.append(deal)

        return deals

    def push_records(self, deals: List[Dict[str, Any]], field_mapping: Dict[str, str]) -> Dict[str, Any]:
        existing_pages = self._query_all_pages()

        client_field = field_mapping.get('client', 'Name')
        existing_by_client = {}
        for page in existing_pages:
            prop = page.get('properties', {}).get(client_field)
            name = _extract_notion_value(prop)
            if name:
                existing_by_client[name] = page['id']

        created_count = 0
        updated_count = 0
        errors = []

        for deal in deals:
            client_name = deal.get('client', '')

            properties = {}
            for crm_field, external_field in field_mapping.items():
                value = deal.get(crm_field)
                notion_prop = _build_notion_property(crm_field, value)
                if notion_prop:
                    properties[external_field] = notion_prop

            try:
                if client_name in existing_by_client:
                    page_id = existing_by_client[client_name]
                    resp = requests.patch(
                        f"{NOTION_API_BASE}/pages/{page_id}",
                        headers=self._headers(),
                        json={"properties": properties}
                    )
                    resp.raise_for_status()
                    updated_count += 1
                else:
                    resp = requests.post(
                        f"{NOTION_API_BASE}/pages",
                        headers=self._headers(),
                        json={
                            "parent": {"database_id": self.database_id},
                            "properties": properties
                        }
                    )
                    resp.raise_for_status()
                    created_count += 1

                time.sleep(0.35)  # Respecter rate limit 3 RPS

            except Exception as e:
                errors.append(f"Erreur pour '{client_name}': {str(e)}")

        return {
            "records_created": created_count,
            "records_updated": updated_count,
            "errors": errors
        }
