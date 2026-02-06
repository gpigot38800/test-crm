## ADDED Requirements

### Requirement: Exposition KPIs via API REST
Le système SHALL exposer les KPIs calculés via endpoint GET /api/kpis retournant JSON au lieu de composants Streamlit tout en réutilisant la logique de calcul existante.

#### Scenario: Endpoint KPIs
- **WHEN** un client envoie GET /api/kpis
- **THEN** le système retourne JSON avec pipeline_pondere_total, panier_moyen, nombre_deals, deals_gagnes et taux_conversion

#### Scenario: Réutilisation calculators pour pipeline
- **WHEN** l'API calcule le pipeline pondéré
- **THEN** le système utilise business_logic/calculators.py::calculate_total_pipeline()

#### Scenario: Calcul panier moyen
- **WHEN** l'API calcule le panier moyen
- **THEN** le système calcule la moyenne de montant_brut via pandas mean()

#### Scenario: Calcul taux conversion
- **WHEN** l'API calcule le taux de conversion
- **THEN** le système divise le nombre de deals gagnés par le total et multiplie par 100

#### Scenario: Formatage valeurs
- **WHEN** les KPIs sont calculés
- **THEN** le système formate les montants avec utils/formatters.py::format_currency()
