"""
Modèle de données pour la table deals.
Définit les constantes utilisées dans toute l'application.
"""

# Nom de la table
TABLE_NAME = "deals"

# Colonnes de la table deals
COLUMNS = [
    "id",
    "client",
    "statut",
    "montant_brut",
    "probabilite",
    "valeur_ponderee",
    "secteur",
    "date_echeance",
    "assignee",
    "notes"
]

# Colonnes requises pour l'insertion
REQUIRED_COLUMNS = [
    "client",
    "statut",
    "montant_brut",
    "probabilite",
    "valeur_ponderee"
]

# Colonnes optionnelles
OPTIONAL_COLUMNS = [
    "secteur",
    "date_echeance",
    "assignee",
    "notes"
]
