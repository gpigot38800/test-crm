## ADDED Requirements

### Requirement: API REST Flask avec blueprints
Le système SHALL fournir une API REST Flask organisée en blueprints pour exposer les données CRM avec endpoints JSON.

#### Scenario: Récupération de tous les deals
- **WHEN** un client envoie GET /api/deals
- **THEN** le système retourne un JSON avec success: true et data contenant la liste complète des deals

#### Scenario: Récupération des KPIs
- **WHEN** un client envoie GET /api/kpis
- **THEN** le système retourne un JSON avec pipeline pondéré total, panier moyen, nombre de deals et taux de conversion

#### Scenario: Analyse par secteur
- **WHEN** un client envoie GET /api/analytics/sectors
- **THEN** le système retourne un JSON avec montants totaux par secteur, paniers moyens et statistiques

#### Scenario: Analyse des échéances
- **WHEN** un client envoie GET /api/analytics/deadlines
- **THEN** le système retourne un JSON avec deals en retard et deals à venir dans les 30 jours

### Requirement: Gestion d'erreurs API
Le système SHALL retourner des codes HTTP appropriés et des messages d'erreur JSON structurés.

#### Scenario: Erreur serveur
- **WHEN** une erreur se produit côté serveur
- **THEN** le système retourne HTTP 500 avec JSON {success: false, error: "message d'erreur"}

#### Scenario: Ressource non trouvée
- **WHEN** un client demande une ressource inexistante
- **THEN** le système retourne HTTP 404 avec JSON {success: false, error: "Resource not found"}

### Requirement: Réutilisation logique métier existante
Le système SHALL réutiliser sans modification les modules database/, business_logic/ et utils/ existants.

#### Scenario: Appel aux fonctions de calcul
- **WHEN** l'API calcule les KPIs
- **THEN** le système utilise business_logic/calculators.py sans modification

#### Scenario: Accès à la base de données
- **WHEN** l'API récupère des deals
- **THEN** le système utilise database/crud.py::get_all_deals() sans modification
