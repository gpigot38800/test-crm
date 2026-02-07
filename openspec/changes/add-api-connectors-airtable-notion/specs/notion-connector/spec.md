## ADDED Requirements

### Requirement: Notion authentication via integration token
Le système SHALL s'authentifier auprès de l'API Notion en utilisant un integration token stocké dans la table connector_configs.

#### Scenario: Authentification réussie
- **WHEN** le système initialise une connexion Notion avec un integration token valide
- **THEN** le système crée une instance notion_client Client et retourne un statut de connexion réussie

#### Scenario: Authentification échouée
- **WHEN** le système tente de se connecter avec un token invalide ou révoqué
- **THEN** le système retourne une erreur avec le message "Token Notion invalide ou révoqué" sans exposer le token dans le message d'erreur

### Requirement: Fetch pages from Notion database
Le système SHALL récupérer toutes les pages d'une base de données Notion configurée et les convertir en format deal CRM.

#### Scenario: Récupération de toutes les pages
- **WHEN** le système exécute un import depuis Notion avec un database_id configuré
- **THEN** le système utilise notion.databases.query() pour récupérer toutes les pages avec gestion de la pagination via start_cursor

#### Scenario: Conversion des propriétés Notion vers champs CRM
- **WHEN** une page Notion est récupérée avec des propriétés title, number, date et select
- **THEN** le système extrait les valeurs selon le field_mapping : title[0].text.content → client, number → montant_brut, date.start → date_echeance, select.name → statut, rich_text[0].text.content → notes/secteur/assignee

#### Scenario: Propriété manquante dans la page Notion
- **WHEN** une page Notion ne contient pas une propriété mappée ou la propriété est vide
- **THEN** le système assigne None au champ CRM correspondant et continue le traitement

#### Scenario: Gestion de la pagination Notion
- **WHEN** la base Notion contient plus de 100 pages (limite par requête)
- **THEN** le système itère avec start_cursor pour récupérer toutes les pages jusqu'à has_more: false

### Requirement: Import deals from Notion to CRM
Le système SHALL importer les deals depuis Notion vers la base de données CRM en appliquant la stratégie "dernière écriture gagne".

#### Scenario: Import avec création de nouveaux deals
- **WHEN** le système importe des pages Notion et qu'une page a un titre (client) qui n'existe pas dans le CRM
- **THEN** le système crée un nouveau deal via insert_deal() avec calcul automatique de probabilité et valeur_ponderee selon le statut

#### Scenario: Import avec mise à jour de deals existants
- **WHEN** le système importe des pages Notion et qu'une page a un titre (client) qui existe déjà dans le CRM
- **THEN** le système met à jour le deal existant via update_deal() avec les nouvelles valeurs et recalcule probabilité et valeur_ponderee

#### Scenario: Normalisation automatique des statuts anglais vers français
- **WHEN** une page Notion a un statut (select ou status) en anglais (ex: "Qualified", "Negotiation", "Won", "Closed Won")
- **THEN** le système normalise automatiquement le statut vers l'équivalent français (qualifié, négociation, gagné) avant l'insertion, garantissant le calcul correct de probabilité et valeur_ponderee

#### Scenario: Statut inconnu lors de l'import
- **WHEN** une page Notion a un statut qui ne correspond ni aux statuts français ni aux statuts anglais connus
- **THEN** le système assigne le statut "prospect" par défaut (probabilité 10%), logge un warning, et inclut cette page dans le décompte du résumé d'import avec mention du statut non reconnu

#### Scenario: Import partiel en cas d'erreur sur une page
- **WHEN** une page Notion échoue à la conversion (ex: propriété number contenant du texte)
- **THEN** le système continue l'import des autres pages, log l'erreur pour la page en échec, et retourne un statut "partial" avec le décompte des succès et échecs

### Requirement: Export deals from CRM to Notion
Le système SHALL exporter les deals du CRM vers une base de données Notion en créant ou mettant à jour les pages.

#### Scenario: Export avec création de nouvelles pages
- **WHEN** le système exporte des deals CRM et qu'un deal a un nom de client qui n'existe pas dans la base Notion
- **THEN** le système crée une nouvelle page via notion.pages.create() avec les propriétés formatées selon les types Notion (title, number, date, select, rich_text)

#### Scenario: Export avec mise à jour de pages existantes
- **WHEN** le système exporte des deals CRM et qu'un deal a un nom de client qui existe déjà dans la base Notion
- **THEN** le système met à jour la page existante via notion.pages.update() avec les propriétés modifiées

#### Scenario: Construction correcte des propriétés Notion
- **WHEN** le système construit les propriétés pour une page Notion à partir d'un deal CRM
- **THEN** le système formate chaque valeur selon le type Notion attendu : client en title, montant_brut en number, date_echeance en date avec start ISO, statut en select, notes en rich_text

### Requirement: Test Notion connection
Le système SHALL permettre de tester la connexion Notion avant d'effectuer des opérations de synchronisation.

#### Scenario: Test de connexion réussi
- **WHEN** le système teste la connexion avec un token et database_id valides
- **THEN** le système retourne un JSON avec success: true, le titre de la database, et le nombre de pages disponibles

#### Scenario: Test de connexion échoué - database non partagée
- **WHEN** le système teste la connexion avec un database_id dont l'intégration n'a pas accès
- **THEN** le système retourne un JSON avec success: false et le message "Base de données Notion inaccessible. Vérifiez que l'intégration est connectée à la page."
