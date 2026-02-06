## ADDED Requirements

### Requirement: Adaptation traitement CSV pour Flask
Le système SHALL adapter le traitement CSV pour fonctionner via endpoint POST Flask au lieu du widget Streamlit tout en conservant la logique de validation existante.

#### Scenario: Réception FormData
- **WHEN** Flask reçoit POST /api/upload/csv avec FormData contenant un fichier
- **THEN** le système extrait le fichier via request.files['file']

#### Scenario: Lecture fichier en mémoire
- **WHEN** le fichier CSV est reçu
- **THEN** le système lit le contenu avec pandas.read_csv() depuis le stream mémoire

#### Scenario: Réutilisation validators
- **WHEN** le CSV est parsé
- **THEN** le système utilise business_logic/validators.py sans modification pour validation

#### Scenario: Réutilisation calculators
- **WHEN** les deals sont validés
- **THEN** le système utilise business_logic/calculators.py pour calcul probabilités et pondérations
