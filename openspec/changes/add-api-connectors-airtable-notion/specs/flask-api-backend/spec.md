## ADDED Requirements

### Requirement: Connector configuration endpoints
Le système SHALL exposer des endpoints REST pour gérer la configuration des connecteurs API.

#### Scenario: Récupération de toutes les configurations
- **WHEN** un client envoie GET /api/connectors/config
- **THEN** le système retourne un JSON avec success: true et data contenant la liste des configurations de connecteurs, avec le champ api_token masqué ("***") pour chaque connecteur configuré

#### Scenario: Sauvegarde de la configuration d'un connecteur
- **WHEN** un client envoie PUT /api/connectors/config/airtable avec un JSON contenant api_token, base_id, table_name et field_mapping
- **THEN** le système crée ou met à jour la configuration en base et retourne HTTP 200 avec success: true

#### Scenario: Sauvegarde sans modifier le token
- **WHEN** un client envoie PUT /api/connectors/config/airtable sans le champ api_token
- **THEN** le système met à jour les autres champs en conservant le token existant en base

#### Scenario: Provider invalide
- **WHEN** un client envoie PUT /api/connectors/config/hubspot (provider non supporté)
- **THEN** le système retourne HTTP 400 avec JSON {success: false, error: "Provider non supporté. Valeurs acceptées: airtable, notion"}

### Requirement: Connection test endpoint
Le système SHALL exposer un endpoint POST pour tester la connexion à un service externe.

#### Scenario: Test de connexion réussi
- **WHEN** un client envoie POST /api/connectors/test/airtable
- **THEN** le système utilise le connecteur approprié pour tester la connexion et retourne HTTP 200 avec success: true et les détails de connexion (nom de table, nombre de records)

#### Scenario: Test de connexion échoué
- **WHEN** un client envoie POST /api/connectors/test/notion et la connexion échoue
- **THEN** le système retourne HTTP 200 avec success: false et le message d'erreur du connecteur

#### Scenario: Test sans configuration existante
- **WHEN** un client envoie POST /api/connectors/test/airtable et qu'aucune configuration n'existe pour ce provider
- **THEN** le système retourne HTTP 400 avec JSON {success: false, error: "Aucune configuration trouvée pour airtable. Configurez d'abord le connecteur."}

### Requirement: Sync import endpoint
Le système SHALL exposer un endpoint POST pour importer les deals depuis un service externe vers le CRM.

#### Scenario: Import réussi
- **WHEN** un client envoie POST /api/sync/airtable/import
- **THEN** le système exécute l'import via le connecteur, crée un sync_log avec le résultat, et retourne HTTP 200 avec success: true et le décompte des records créés, mis à jour et en erreur

#### Scenario: Import avec erreurs partielles
- **WHEN** un client envoie POST /api/sync/notion/import et certains records échouent à la validation
- **THEN** le système retourne HTTP 200 avec success: true, status: "partial", et le décompte détaillé

#### Scenario: Import échoué - erreur de connexion
- **WHEN** un client envoie POST /api/sync/airtable/import et la connexion au service échoue
- **THEN** le système crée un sync_log avec status "error", et retourne HTTP 500 avec success: false et le message d'erreur

### Requirement: Sync export endpoint
Le système SHALL exposer un endpoint POST pour exporter les deals du CRM vers un service externe.

#### Scenario: Export réussi
- **WHEN** un client envoie POST /api/sync/notion/export
- **THEN** le système récupère tous les deals du CRM, les exporte via le connecteur, crée un sync_log, et retourne HTTP 200 avec success: true et le décompte

#### Scenario: Export avec base CRM vide
- **WHEN** un client envoie POST /api/sync/airtable/export et qu'il n'y a aucun deal dans le CRM
- **THEN** le système retourne HTTP 200 avec success: true, records_processed: 0 et un message "Aucun deal à exporter"

### Requirement: Sync logs endpoint
Le système SHALL exposer un endpoint GET pour récupérer l'historique des synchronisations.

#### Scenario: Récupération des logs
- **WHEN** un client envoie GET /api/sync/logs
- **THEN** le système retourne un JSON avec success: true et data contenant les 50 derniers sync_logs triés par started_at descendant

#### Scenario: Filtrage des logs par provider
- **WHEN** un client envoie GET /api/sync/logs?provider=airtable
- **THEN** le système retourne uniquement les logs du provider Airtable

### Requirement: Database schema for connector tables
Le système SHALL créer les tables connector_configs et sync_logs lors de l'initialisation de la base de données.

#### Scenario: Création de la table connector_configs
- **WHEN** l'application démarre et initialise la base de données
- **THEN** le système crée la table connector_configs avec les colonnes id, provider (UNIQUE), api_token, base_id, table_name, field_mapping (JSON texte), is_active (boolean), updated_at

#### Scenario: Création de la table sync_logs
- **WHEN** l'application démarre et initialise la base de données
- **THEN** le système crée la table sync_logs avec les colonnes id, provider, direction, status, records_processed, records_created, records_updated, error_message, started_at, completed_at

#### Scenario: Tables existantes non recréées
- **WHEN** l'application redémarre et les tables existent déjà
- **THEN** le système utilise CREATE TABLE IF NOT EXISTS et ne détruit pas les données existantes

### Requirement: Sync blueprint registration
Le système SHALL enregistrer un nouveau blueprint Flask sync_bp dans l'application pour regrouper tous les endpoints de synchronisation.

#### Scenario: Enregistrement du blueprint
- **WHEN** l'application Flask démarre
- **THEN** le système enregistre sync_bp avec url_prefix='/api' dans register_blueprints()

#### Scenario: Coexistence avec les blueprints existants
- **WHEN** les endpoints sync sont enregistrés
- **THEN** les endpoints existants (deals_bp, analytics_bp, upload_bp) continuent de fonctionner sans modification
