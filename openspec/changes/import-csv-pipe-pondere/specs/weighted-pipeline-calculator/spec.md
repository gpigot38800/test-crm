## Purpose

Calculer automatiquement les probabilités de conversion selon le statut de chaque deal, calculer la valeur pondérée correspondante, et afficher le pipeline pondéré total pour prévoir le CA réel.

## ADDED Requirements

### Requirement: Probability Calculation by Status
Le système DOIT calculer automatiquement la probabilité de conversion selon le statut du deal.

#### Scenario: Prospect status probability
- **WHEN** un deal a le statut "Prospect"
- **THEN** le système assigne une probabilité de 0.10 (10%)

#### Scenario: Qualified status probability
- **WHEN** un deal a le statut "Qualifié"
- **THEN** le système assigne une probabilité de 0.30 (30%)

#### Scenario: Negotiation status probability
- **WHEN** un deal a le statut "Négociation"
- **THEN** le système assigne une probabilité de 0.70 (70%)

#### Scenario: Won status probability
- **WHEN** un deal a le statut "Gagné"
- **THEN** le système assigne une probabilité de 1.00 (100%)

#### Scenario: Case insensitive status matching
- **WHEN** un deal a le statut "PROSPECT" ou "prospect" ou "Prospect"
- **THEN** le système normalise en minuscules et assigne la probabilité de 0.10

#### Scenario: Unrecognized status default
- **WHEN** un deal a un statut non reconnu après normalisation
- **THEN** le système assigne par défaut une probabilité de 0.10 et log un avertissement

### Requirement: Weighted Value Calculation
Le système DOIT calculer la valeur pondérée pour chaque deal en multipliant le montant brut par la probabilité.

#### Scenario: Standard weighted value calculation
- **WHEN** un deal a un montant_brut de 50000€ et une probabilité de 0.30
- **THEN** le système calcule une valeur_ponderee de 15000.00€

#### Scenario: Rounding to 2 decimals
- **WHEN** le calcul de valeur_ponderee produit plus de 2 décimales (ex: 33333.333...)
- **THEN** le système arrondit à 2 décimales (33333.33€)

#### Scenario: Zero amount handling
- **WHEN** un deal a un montant_brut de 0€
- **THEN** le système calcule une valeur_ponderee de 0.00€

#### Scenario: Won deal full value
- **WHEN** un deal "Gagné" a un montant_brut de 100000€ et probabilité de 1.00
- **THEN** le système calcule une valeur_ponderee de 100000.00€ (montant complet)

### Requirement: Pipeline Pondéré Total Display
Le système DOIT afficher le pipeline pondéré total comme KPI principal du dashboard.

#### Scenario: Single deal pipeline
- **WHEN** la base contient un seul deal avec valeur_ponderee de 20000€
- **THEN** le système affiche "Pipeline Pondéré Total: 20 000 €"

#### Scenario: Multiple deals aggregation
- **WHEN** la base contient 5 deals avec valeurs_ponderees [10000, 20000, 30000, 15000, 5000]
- **THEN** le système affiche "Pipeline Pondéré Total: 80 000 €"

#### Scenario: Empty database
- **WHEN** la table deals est vide
- **THEN** le système affiche "Pipeline Pondéré Total: 0 €"

#### Scenario: Formatting with thousand separators
- **WHEN** le pipeline total est de 1500000€
- **THEN** le système affiche "Pipeline Pondéré Total: 1 500 000 €" avec séparateurs de milliers

### Requirement: KPI Metric Component
Le système DOIT utiliser un composant Streamlit st.metric() pour afficher le pipeline pondéré.

#### Scenario: Metric with label and value
- **WHEN** le pipeline total est calculé
- **THEN** le système affiche un widget st.metric avec label "Pipeline Pondéré Total" et la valeur formatée

#### Scenario: Metric with help text
- **WHEN** l'utilisateur survole l'icône d'aide du metric
- **THEN** le système affiche le tooltip "Somme des valeurs pondérées (montant × probabilité)"

### Requirement: Real-time Recalculation
Le système DOIT recalculer automatiquement le pipeline pondéré lors de chaque modification des données.

#### Scenario: Post-import recalculation
- **WHEN** un nouvel import CSV est effectué
- **THEN** le système recalcule immédiatement le pipeline pondéré avec les nouvelles données

#### Scenario: Page refresh
- **WHEN** l'utilisateur rafraîchit la page Streamlit
- **THEN** le système recharge les deals depuis la base et recalcule le pipeline pondéré

### Requirement: Probability Mapping Constants
Le système DOIT définir les probabilités dans un fichier de constantes pour faciliter la maintenance.

#### Scenario: Constants file usage
- **WHEN** le calculateur a besoin de la probabilité pour un statut
- **THEN** le système consulte le dictionnaire PROBABILITY_MAP défini dans utils/constants.py

#### Scenario: Single source of truth
- **WHEN** les probabilités doivent être modifiées (ex: changement règle métier)
- **THEN** seul le fichier constants.py nécessite une modification (pas de duplication dans le code)

### Requirement: Calculation Performance
Le système DOIT calculer le pipeline pondéré en moins de 100ms pour des datasets de moins de 1000 deals.

#### Scenario: In-memory calculation
- **WHEN** le calcul du pipeline est déclenché avec 500 deals en mémoire (DataFrame Pandas)
- **THEN** le système effectue la somme en moins de 50ms

#### Scenario: No database query for aggregation
- **WHEN** le pipeline doit être calculé
- **THEN** le système utilise les données déjà chargées en mémoire (pas de requête SQL SELECT SUM())
