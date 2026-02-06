## ADDED Requirements

### Requirement: Exposition analyse secteurs via API REST
Le système SHALL exposer l'analyse par secteur via endpoint GET /api/analytics/sectors retournant JSON pour Chart.js au lieu de graphiques Plotly/Streamlit.

#### Scenario: Endpoint analytics secteurs
- **WHEN** un client envoie GET /api/analytics/sectors
- **THEN** le système retourne JSON avec sector_totals, sector_averages, top_5_avg et summary_table

#### Scenario: Calcul montants totaux par secteur
- **WHEN** l'API calcule les montants par secteur
- **THEN** le système groupe les deals par secteur et somme montant_brut via pandas groupby().sum()

#### Scenario: Calcul paniers moyens par secteur
- **WHEN** l'API calcule les paniers moyens
- **THEN** le système groupe les deals par secteur et calcule mean() de montant_brut

#### Scenario: Top 5 secteurs meilleurs paniers
- **WHEN** l'API calcule le top 5
- **THEN** le système trie les secteurs par panier moyen décroissant et prend les 5 premiers

#### Scenario: Tableau récapitulatif
- **WHEN** l'API génère le tableau récapitulatif
- **THEN** le système retourne pour chaque secteur : montant_total, panier_moyen, nombre_deals et valeur_ponderee

#### Scenario: Formatage données pour Chart.js
- **WHEN** les données secteurs sont retournées
- **THEN** le système structure le JSON avec labels (noms secteurs) et datasets (valeurs) compatibles Chart.js
