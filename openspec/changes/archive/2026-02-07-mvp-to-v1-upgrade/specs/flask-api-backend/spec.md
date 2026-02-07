## ADDED Requirements

### Requirement: Create deal endpoint
Le système SHALL exposer un endpoint POST /api/deals permettant de créer un deal individuel à partir de données JSON.

#### Scenario: Création de deal réussie
- **WHEN** un client envoie POST /api/deals avec un JSON contenant client, statut et montant_brut valides
- **THEN** le système calcule automatiquement la probabilité et la valeur pondérée, insère le deal en base, et retourne HTTP 201 avec le deal créé incluant son id

#### Scenario: Création avec données invalides
- **WHEN** un client envoie POST /api/deals avec des données invalides (client vide ou montant <= 0)
- **THEN** le système retourne HTTP 400 avec JSON {success: false, error: "détail des erreurs de validation"}

#### Scenario: Création avec champs optionnels
- **WHEN** un client envoie POST /api/deals avec uniquement les champs requis (client, statut, montant_brut)
- **THEN** le système crée le deal avec les champs optionnels (secteur, date_echeance, assignee, notes) à null

### Requirement: Update deal endpoint
Le système SHALL exposer un endpoint PUT /api/deals/<id> permettant de modifier un deal existant.

#### Scenario: Modification de deal réussie
- **WHEN** un client envoie PUT /api/deals/5 avec des données JSON valides
- **THEN** le système met à jour le deal id=5, recalcule probabilité et valeur pondérée si le statut a changé, et retourne HTTP 200 avec le deal modifié

#### Scenario: Modification d'un deal inexistant
- **WHEN** un client envoie PUT /api/deals/999 et l'id 999 n'existe pas en base
- **THEN** le système retourne HTTP 404 avec JSON {success: false, error: "Deal non trouvé"}

#### Scenario: Modification avec données invalides
- **WHEN** un client envoie PUT /api/deals/5 avec un montant <= 0
- **THEN** le système retourne HTTP 400 avec JSON {success: false, error: "détail des erreurs"}

### Requirement: Delete single deal endpoint
Le système SHALL exposer un endpoint DELETE /api/deals/<id> permettant de supprimer un deal individuel.

#### Scenario: Suppression réussie
- **WHEN** un client envoie DELETE /api/deals/5 et le deal id=5 existe
- **THEN** le système supprime le deal et retourne HTTP 200 avec JSON {success: true, data: {message: "Deal supprimé"}}

#### Scenario: Suppression d'un deal inexistant
- **WHEN** un client envoie DELETE /api/deals/999 et l'id 999 n'existe pas
- **THEN** le système retourne HTTP 404 avec JSON {success: false, error: "Deal non trouvé"}

### Requirement: Performance analytics endpoint
Le système SHALL exposer un endpoint GET /api/analytics/performance retournant les métriques par commercial.

#### Scenario: Récupération des performances
- **WHEN** un client envoie GET /api/analytics/performance
- **THEN** le système retourne un JSON avec pour chaque assignee : nb_deals, montant_total, pipeline_pondere, deals_gagnes, taux_conversion, panier_moyen

#### Scenario: Données Chart.js compatibles
- **WHEN** un client envoie GET /api/analytics/performance
- **THEN** le JSON retourné inclut un objet chart_data avec labels (noms des assignees) et datasets formatés pour Chart.js

### Requirement: Filter query parameters on existing endpoints
Le système SHALL accepter des query parameters optionnels de filtrage sur tous les endpoints existants (GET /api/deals, GET /api/kpis, GET /api/analytics/sectors, GET /api/analytics/deadlines) et le nouvel endpoint performance.

#### Scenario: Filtrage par statut
- **WHEN** un client envoie GET /api/kpis?statut=Négociation
- **THEN** le système retourne les KPIs calculés uniquement sur les deals en Négociation

#### Scenario: Filtrage multiple
- **WHEN** un client envoie GET /api/deals?statut=Prospect&secteur=Tech&assignee=Alice
- **THEN** le système retourne uniquement les deals Prospect du secteur Tech assignés à Alice

#### Scenario: Filtrage par plage de dates
- **WHEN** un client envoie GET /api/deals?date_from=2025-01-01&date_to=2025-06-30
- **THEN** le système retourne uniquement les deals avec date_echeance entre le 1er janvier et le 30 juin 2025

#### Scenario: Recherche textuelle
- **WHEN** un client envoie GET /api/deals?search=Acme
- **THEN** le système retourne uniquement les deals dont le client ou les notes contiennent "Acme" (insensible à la casse)

#### Scenario: Sans query parameters (rétro-compatibilité)
- **WHEN** un client envoie GET /api/deals sans query parameters
- **THEN** le système retourne tous les deals comme avant (comportement identique au MVP)

### Requirement: Filter options endpoint
Le système SHALL exposer un endpoint GET /api/filters/options retournant les valeurs disponibles pour les filtres.

#### Scenario: Récupération des options de filtres
- **WHEN** un client envoie GET /api/filters/options
- **THEN** le système retourne un JSON avec les listes distinctes de statuts, secteurs et assignees présents en base

## MODIFIED Requirements

### Requirement: Réutilisation logique métier existante
Le système SHALL réutiliser les modules database/, business_logic/ et utils/ existants, en les étendant avec de nouvelles fonctions pour le CRUD individuel, les calculs de performance et le filtrage.

#### Scenario: Appel aux fonctions de calcul
- **WHEN** l'API calcule les KPIs
- **THEN** le système utilise business_logic/calculators.py

#### Scenario: Accès à la base de données
- **WHEN** l'API récupère des deals
- **THEN** le système utilise database/crud.py

#### Scenario: Nouvelles fonctions CRUD
- **WHEN** l'API crée, modifie ou supprime un deal individuel
- **THEN** le système utilise les nouvelles fonctions insert_deal(), update_deal(), delete_deal(), get_deal_by_id() de database/crud.py

#### Scenario: Filtrage en base de données
- **WHEN** l'API reçoit des query parameters de filtrage
- **THEN** le système utilise la nouvelle fonction get_filtered_deals() de database/crud.py qui construit des clauses WHERE avec paramètres liés
