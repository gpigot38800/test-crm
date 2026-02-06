"""
Constantes globales de l'application.
Définit les probabilités par statut et les valeurs valides.
"""

# Mapping des probabilités par statut
PROBABILITY_MAP = {
    'prospect': 0.10,
    'qualifié': 0.30,
    'négociation': 0.70,
    'gagné': 1.00,
    'gagné - en cours': 1.00  # Traité comme gagné
}

# Statuts valides (pour validation) - case insensitive
VALID_STATUSES = [
    'prospect',
    'qualifié',
    'négociation',
    'gagné',
    'gagné - en cours'  # Variante trouvée dans le CSV demo
]

# Mapping des colonnes CSV vers schéma DB
CSV_TO_DB_COLUMNS = {
    'task name': 'client',
    'status': 'statut',
    'montant deal': 'montant_brut',
    'tags': 'secteur',
    'due date': 'date_echeance',
    'assignees': 'assignee',
    'task content': 'notes'
}
