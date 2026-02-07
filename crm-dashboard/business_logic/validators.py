"""
Fonctions de validation des données CSV et des deals.
Valide la structure CSV et les règles métier pour chaque deal.
"""

import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dateutil import parser
from utils.constants import VALID_STATUSES


class ValidationError:
    """Classe pour stocker les erreurs de validation"""

    def __init__(self, row_number: int, field: str, message: str):
        self.row_number = row_number
        self.field = field
        self.message = message

    def __repr__(self):
        return f"Ligne {self.row_number} - {self.field}: {self.message}"


def validate_csv_structure(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Valide la structure du DataFrame CSV (colonnes requises présentes).

    Args:
        df: DataFrame pandas à valider (déjà normalisé)

    Returns:
        Tuple[bool, List[str]]: (True si valide, liste des colonnes manquantes)
    """
    # Colonnes requises en CSV normalisé (lowercase, après normalisation, avant mapping)
    # Ces colonnes correspondent au fichier CSV réel
    required_columns = ['task name', 'status', 'montant deal']

    # Les colonnes sont déjà normalisées (lowercase) lors de l'appel
    df_columns_normalized = list(df.columns)

    # Vérifier les colonnes manquantes
    missing_columns = []
    for col in required_columns:
        if col not in df_columns_normalized:
            missing_columns.append(col)

    is_valid = len(missing_columns) == 0

    return is_valid, missing_columns


def validate_deal_row(row: pd.Series, row_number: int) -> List[ValidationError]:
    """
    Valide une ligne de deal selon les règles métier.

    Args:
        row: Ligne du DataFrame (pd.Series)
        row_number: Numéro de la ligne (pour reporting d'erreurs)

    Returns:
        List[ValidationError]: Liste des erreurs de validation (vide si valide)
    """
    errors = []

    # Validation 1: Client non vide
    if pd.isna(row.get('client')) or str(row.get('client')).strip() == '':
        errors.append(ValidationError(
            row_number,
            'client',
            'Le nom du client ne peut pas être vide'
        ))

    # Validation 2: Statut valide (case-insensitive)
    statut = str(row.get('statut', '')).strip().lower()
    if statut not in VALID_STATUSES:
        errors.append(ValidationError(
            row_number,
            'statut',
            f'Statut invalide. Valeurs acceptées: {", ".join(VALID_STATUSES)}'
        ))

    # Validation 3: Montant > 0
    try:
        montant = float(row.get('montant_brut', 0))
        if montant <= 0:
            errors.append(ValidationError(
                row_number,
                'montant_brut',
                'Le montant doit être supérieur à 0'
            ))
    except (ValueError, TypeError):
        errors.append(ValidationError(
            row_number,
            'montant_brut',
            'Le montant doit être un nombre valide'
        ))

    # Validation 4: Date échéance valide (si présente)
    if not pd.isna(row.get('date_echeance')):
        date_str = str(row.get('date_echeance'))
        parsed_date = parse_date(date_str)
        if parsed_date is None:
            errors.append(ValidationError(
                row_number,
                'date_echeance',
                'Format de date invalide. Formats acceptés: YYYY-MM-DD, DD/MM/YYYY'
            ))

    return errors


def parse_date(date_str: str) -> Optional[str]:
    """
    Parse une date string en supportant plusieurs formats.

    Args:
        date_str: String de date à parser

    Returns:
        Optional[str]: Date au format ISO (YYYY-MM-DD) ou None si parsing échoue
    """
    if not date_str or pd.isna(date_str):
        return None

    try:
        # Utiliser dateutil.parser avec dayfirst=True (format européen)
        parsed_date = parser.parse(str(date_str).strip(), dayfirst=True)
        return parsed_date.strftime('%Y-%m-%d')

    except (ValueError, parser.ParserError):
        return None


def validate_deal_dict(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Valide un dictionnaire de deal (entrée formulaire ou API JSON).

    Args:
        data: Dictionnaire contenant les champs du deal

    Returns:
        Tuple[bool, List[str]]: (True si valide, liste des messages d'erreur)
    """
    errors = []

    # Client non vide
    client = data.get('client', '')
    if not client or str(client).strip() == '':
        errors.append("Le nom du client ne peut pas être vide")

    # Statut valide
    statut = str(data.get('statut', '')).strip().lower()
    if statut not in VALID_STATUSES:
        errors.append(f"Statut invalide. Valeurs acceptées: {', '.join(VALID_STATUSES)}")

    # Montant > 0
    try:
        montant = float(data.get('montant_brut', 0))
        if montant <= 0:
            errors.append("Le montant doit être supérieur à 0")
    except (ValueError, TypeError):
        errors.append("Le montant doit être un nombre valide")

    # Date échéance valide (si présente)
    date_echeance = data.get('date_echeance')
    if date_echeance and str(date_echeance).strip():
        parsed = parse_date(str(date_echeance))
        if parsed is None:
            errors.append("Format de date invalide. Formats acceptés: YYYY-MM-DD, DD/MM/YYYY")

    is_valid = len(errors) == 0
    return is_valid, errors


def get_validation_summary(errors: List[ValidationError]) -> str:
    """
    Génère un résumé des erreurs de validation pour affichage.

    Args:
        errors: Liste des erreurs de validation

    Returns:
        str: Résumé formaté des erreurs
    """
    if not errors:
        return "Aucune erreur de validation"

    summary = f"Total: {len(errors)} erreur(s) détectée(s)\n\n"
    for error in errors:
        summary += f"- {error}\n"

    return summary
