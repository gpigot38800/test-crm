"""
Gestion du mapping des champs entre le CRM et les services externes.
Inclut la normalisation des statuts anglais → français.
"""

import json
import logging
from typing import Dict, Any, Optional

from utils.constants import VALID_STATUSES, STATUS_NORMALIZATION_MAP

logger = logging.getLogger(__name__)

# Mapping par défaut CRM → service externe
DEFAULT_FIELD_MAPPING = {
    "client": "Name",
    "statut": "Status",
    "montant_brut": "Amount",
    "secteur": "Sector",
    "date_echeance": "Due Date",
    "assignee": "Assignee",
    "notes": "Notes"
}


def get_field_mapping(config: Dict[str, Any]) -> Dict[str, str]:
    """
    Retourne le mapping des champs depuis la config du connecteur.
    Utilise le mapping par défaut si aucun n'est configuré.
    """
    raw = config.get('field_mapping')
    if raw:
        if isinstance(raw, str):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                logger.warning("field_mapping JSON invalide, utilisation du défaut")
                return DEFAULT_FIELD_MAPPING.copy()
        elif isinstance(raw, dict):
            return raw
    return DEFAULT_FIELD_MAPPING.copy()


def convert_external_to_crm(record: Dict[str, Any], field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    Convertit un record externe en format deal CRM selon le mapping.

    Args:
        record: Record du service externe (clé = nom colonne externe, valeur = donnée)
        field_mapping: Mapping champ_crm → champ_externe

    Returns:
        Dict au format deal CRM
    """
    deal = {}
    # Inverser le mapping : externe → crm
    reverse_mapping = {v: k for k, v in field_mapping.items()}

    for external_field, value in record.items():
        crm_field = reverse_mapping.get(external_field)
        if crm_field:
            deal[crm_field] = value

    return deal


def convert_crm_to_external(deal: Dict[str, Any], field_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    Convertit un deal CRM en format record externe selon le mapping.

    Args:
        deal: Deal au format CRM
        field_mapping: Mapping champ_crm → champ_externe

    Returns:
        Dict au format service externe
    """
    record = {}
    for crm_field, external_field in field_mapping.items():
        value = deal.get(crm_field)
        if value is not None:
            record[external_field] = value
    return record


def normalize_status(statut: str) -> Optional[str]:
    """
    Normalise un statut vers le format français attendu par le CRM.

    1. Vérifie d'abord si le statut correspond directement à un statut valide (français)
    2. Sinon, cherche dans le mapping anglais → français
    3. Retourne None si le statut est inconnu

    Args:
        statut: Statut brut (français, anglais, ou autre)

    Returns:
        Statut normalisé en français, ou None si inconnu
    """
    if not statut:
        return None

    normalized = statut.lower().strip()

    # Match direct avec les statuts français valides
    if normalized in VALID_STATUSES:
        return normalized

    # Traduction anglais → français
    if normalized in STATUS_NORMALIZATION_MAP:
        return STATUS_NORMALIZATION_MAP[normalized]

    logger.warning(f"Statut non reconnu: '{statut}' — ni français ni anglais connu")
    return None
