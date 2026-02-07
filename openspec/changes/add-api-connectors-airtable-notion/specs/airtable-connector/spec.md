## ADDED Requirements

### Requirement: Airtable authentication via Personal Access Token
Le système SHALL s'authentifier auprès de l'API Airtable en utilisant un Personal Access Token (PAT) stocké dans la table connector_configs.

#### Scenario: Authentification réussie
- **WHEN** le système initialise une connexion Airtable avec un PAT valide
- **THEN** le système crée une instance pyairtable Api et retourne un statut de connexion réussie

#### Scenario: Authentification échouée
- **WHEN** le système tente de se connecter avec un PAT invalide ou expiré
- **THEN** le système retourne une erreur avec le message "Token Airtable invalide ou expiré" sans exposer le token dans le message d'erreur

### Requirement: Fetch records from Airtable table
Le système SHALL récupérer tous les records d'une table Airtable configurée et les convertir en format deal CRM.

#### Scenario: Récupération de tous les records
- **WHEN** le système exécute un import depuis Airtable avec une base_id et table_name configurés
- **THEN** le système utilise pyairtable table.all() pour récupérer tous les records avec pagination automatique

#### Scenario: Conversion des types de champs Airtable vers CRM
- **WHEN** un record Airtable est récupéré avec des champs texte, nombre et date
- **THEN** le système convertit les champs selon le field_mapping configuré : texte → client/secteur/assignee/notes, nombre → montant_brut, date → date_echeance, single select → statut

#### Scenario: Champ manquant dans le record Airtable
- **WHEN** un record Airtable ne contient pas un champ mappé (ex: le champ "Notes" est vide)
- **THEN** le système assigne None au champ CRM correspondant et continue le traitement

### Requirement: Import deals from Airtable to CRM
Le système SHALL importer les deals depuis Airtable vers la base de données CRM en appliquant la stratégie "dernière écriture gagne".

#### Scenario: Import avec création de nouveaux deals
- **WHEN** le système importe des records Airtable et qu'un record a un nom de client qui n'existe pas dans le CRM
- **THEN** le système crée un nouveau deal via insert_deal() avec calcul automatique de probabilité et valeur_ponderee selon le statut

#### Scenario: Import avec mise à jour de deals existants
- **WHEN** le système importe des records Airtable et qu'un record a un nom de client qui existe déjà dans le CRM
- **THEN** le système met à jour le deal existant via update_deal() avec les nouvelles valeurs et recalcule probabilité et valeur_ponderee

#### Scenario: Normalisation automatique des statuts anglais vers français
- **WHEN** un record Airtable a un statut en anglais (ex: "Qualified", "Negotiation", "Won", "Closed Won")
- **THEN** le système normalise automatiquement le statut vers l'équivalent français (qualifié, négociation, gagné) avant l'insertion, garantissant le calcul correct de probabilité et valeur_ponderee

#### Scenario: Statut inconnu lors de l'import
- **WHEN** un record Airtable a un statut qui ne correspond ni aux statuts français ni aux statuts anglais connus
- **THEN** le système assigne le statut "prospect" par défaut (probabilité 10%), logge un warning, et inclut ce record dans le décompte du résumé d'import avec mention du statut non reconnu

#### Scenario: Import partiel en cas d'erreur sur un record
- **WHEN** un record Airtable échoue à la validation (ex: montant_brut non numérique)
- **THEN** le système continue l'import des autres records, log l'erreur pour le record en échec, et retourne un statut "partial" avec le décompte des succès et échecs

### Requirement: Export deals from CRM to Airtable
Le système SHALL exporter les deals du CRM vers une table Airtable en créant ou mettant à jour les records.

#### Scenario: Export avec création de nouveaux records
- **WHEN** le système exporte des deals CRM et qu'un deal a un nom de client qui n'existe pas dans la table Airtable
- **THEN** le système crée un nouveau record Airtable via table.create() avec les champs mappés

#### Scenario: Export avec mise à jour de records existants
- **WHEN** le système exporte des deals CRM et qu'un deal a un nom de client qui existe déjà dans la table Airtable
- **THEN** le système met à jour le record Airtable existant via table.update() avec les nouvelles valeurs

#### Scenario: Export batch pour performance
- **WHEN** le système exporte plus de 10 deals vers Airtable
- **THEN** le système utilise table.batch_create() et table.batch_update() pour regrouper les opérations et respecter le rate limiting de 5 QPS

### Requirement: Test Airtable connection
Le système SHALL permettre de tester la connexion Airtable avant d'effectuer des opérations de synchronisation.

#### Scenario: Test de connexion réussi
- **WHEN** le système teste la connexion avec un PAT, base_id et table_name valides
- **THEN** le système retourne un JSON avec success: true, le nom de la table, et le nombre de records disponibles

#### Scenario: Test de connexion échoué - base inexistante
- **WHEN** le système teste la connexion avec un base_id invalide
- **THEN** le système retourne un JSON avec success: false et le message "Base Airtable introuvable"
