"""
Classe abstraite pour les connecteurs API externes.
Définit le contrat commun : test_connection, fetch_records, push_records.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseConnector(ABC):
    """Interface commune pour tous les connecteurs (Airtable, Notion, etc.)."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_token = config.get('api_token', '')
        self.base_id = config.get('base_id', '')
        self.table_name = config.get('table_name', '')

    @abstractmethod
    def test_connection(self) -> Dict[str, Any]:
        """
        Teste la connexion au service externe.

        Returns:
            Dict avec success (bool), message, et détails (nom table, nb records)
        """
        pass

    @abstractmethod
    def fetch_records(self, field_mapping: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        Récupère tous les records du service et les convertit en format deal CRM.

        Args:
            field_mapping: Mapping champ_crm → champ_externe

        Returns:
            Liste de dicts au format deal CRM
        """
        pass

    @abstractmethod
    def push_records(self, deals: List[Dict[str, Any]], field_mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        Pousse des deals CRM vers le service externe.

        Args:
            deals: Liste de deals au format CRM
            field_mapping: Mapping champ_crm → champ_externe

        Returns:
            Dict avec records_created, records_updated, errors
        """
        pass
