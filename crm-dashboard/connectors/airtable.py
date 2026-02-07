"""
Connecteur Airtable : synchronisation bidirectionnelle des deals via API REST.
Utilise requests directement (compatible Python 3.14).
"""

import logging
import time
from typing import Any, Dict, List

import requests

from .base import BaseConnector
from .field_mapping import convert_external_to_crm, convert_crm_to_external

logger = logging.getLogger(__name__)

AIRTABLE_API_BASE = "https://api.airtable.com/v0"


class AirtableConnector(BaseConnector):

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._record_name_cache = None

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def _table_url(self):
        return f"{AIRTABLE_API_BASE}/{self.base_id}/{requests.utils.quote(self.table_name)}"

    def _get_all_records(self) -> List[Dict]:
        """Récupère tous les records avec pagination."""
        records = []
        offset = None
        while True:
            params = {}
            if offset:
                params['offset'] = offset
            resp = requests.get(self._table_url(), headers=self._headers(), params=params)
            resp.raise_for_status()
            data = resp.json()
            records.extend(data.get('records', []))
            offset = data.get('offset')
            if not offset:
                break
        return records

    def _build_record_name_cache(self) -> Dict[str, str]:
        """Construit un cache ID → nom pour résoudre les linked records."""
        if self._record_name_cache is not None:
            return self._record_name_cache

        self._record_name_cache = {}
        try:
            resp = requests.get(
                f"{AIRTABLE_API_BASE}/meta/bases/{self.base_id}/tables",
                headers=self._headers()
            )
            resp.raise_for_status()
            tables = resp.json().get('tables', [])

            for table in tables:
                table_name = table['name']
                if table_name == self.table_name:
                    continue
                fields = table.get('fields', [])
                if not fields:
                    continue
                primary_field = fields[0]['name']

                offset = None
                while True:
                    params = {}
                    if offset:
                        params['offset'] = offset
                    r = requests.get(
                        f"{AIRTABLE_API_BASE}/{self.base_id}/{requests.utils.quote(table_name)}",
                        headers=self._headers(), params=params
                    )
                    if r.status_code != 200:
                        break
                    data = r.json()
                    for rec in data.get('records', []):
                        name = rec.get('fields', {}).get(primary_field)
                        if name:
                            self._record_name_cache[rec['id']] = str(name)
                    offset = data.get('offset')
                    if not offset:
                        break
                    time.sleep(0.2)
                time.sleep(0.2)
        except Exception as e:
            logger.warning(f"Impossible de résoudre les linked records: {e}")

        return self._record_name_cache

    def _clean_field_value(self, value: Any, name_cache: Dict[str, str]) -> Any:
        """Nettoie une valeur Airtable : convertit les listes et résout les IDs."""
        if not isinstance(value, list):
            return value
        resolved = []
        for item in value:
            if isinstance(item, str) and item.startswith('rec'):
                resolved.append(name_cache.get(item, item))
            else:
                resolved.append(str(item))
        return ', '.join(resolved)

    def test_connection(self) -> Dict[str, Any]:
        try:
            records = self._get_all_records()
            return {
                "success": True,
                "message": "Connexion Airtable réussie",
                "table_name": self.table_name,
                "record_count": len(records)
            }
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            if status == 404:
                return {"success": False, "message": "Base Airtable introuvable"}
            if status in (401, 403):
                return {"success": False, "message": "Token Airtable invalide ou expiré"}
            return {"success": False, "message": f"Erreur Airtable HTTP {status}"}
        except Exception as e:
            return {"success": False, "message": f"Erreur connexion Airtable: {str(e)}"}

    def fetch_records(self, field_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
        raw_records = self._get_all_records()
        name_cache = self._build_record_name_cache()

        deals = []
        for record in raw_records:
            fields = record.get('fields', {})

            flat_record = {}
            for crm_field, external_field in field_mapping.items():
                value = fields.get(external_field)
                flat_record[external_field] = self._clean_field_value(value, name_cache)

            deal = convert_external_to_crm(flat_record, field_mapping)

            if deal.get('montant_brut') is not None:
                try:
                    deal['montant_brut'] = float(deal['montant_brut'])
                except (ValueError, TypeError):
                    deal['montant_brut'] = None

            deal['_airtable_id'] = record.get('id')
            deals.append(deal)

        return deals

    def push_records(self, deals: List[Dict[str, Any]], field_mapping: Dict[str, str]) -> Dict[str, Any]:
        existing_records = self._get_all_records()
        client_field = field_mapping.get('client', 'Name')

        existing_by_client = {}
        for rec in existing_records:
            name = rec.get('fields', {}).get(client_field, '')
            if name:
                existing_by_client[name] = rec['id']

        to_create = []
        to_update = []

        for deal in deals:
            external_record = convert_crm_to_external(deal, field_mapping)
            client_name = deal.get('client', '')

            if client_name in existing_by_client:
                to_update.append({
                    "id": existing_by_client[client_name],
                    "fields": external_record
                })
            else:
                to_create.append({"fields": external_record})

        created_count = 0
        updated_count = 0
        errors = []

        # Batch create (max 10 par requête Airtable)
        for i in range(0, len(to_create), 10):
            batch = to_create[i:i+10]
            try:
                resp = requests.post(
                    self._table_url(),
                    headers=self._headers(),
                    json={"records": batch}
                )
                resp.raise_for_status()
                created_count += len(batch)
                time.sleep(0.2)  # Respecter rate limit 5 QPS
            except Exception as e:
                errors.append(f"Erreur batch create: {str(e)}")

        # Batch update (max 10 par requête)
        for i in range(0, len(to_update), 10):
            batch = to_update[i:i+10]
            try:
                resp = requests.patch(
                    self._table_url(),
                    headers=self._headers(),
                    json={"records": batch}
                )
                resp.raise_for_status()
                updated_count += len(batch)
                time.sleep(0.2)
            except Exception as e:
                errors.append(f"Erreur batch update: {str(e)}")

        return {
            "records_created": created_count,
            "records_updated": updated_count,
            "errors": errors
        }
