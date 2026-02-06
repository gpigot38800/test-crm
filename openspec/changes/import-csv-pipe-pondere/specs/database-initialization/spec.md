## Purpose

Initialiser la base de données SQLite avec le schéma requis pour stocker les deals, incluant la création de la table deals avec toutes ses colonnes et la gestion de la connexion database.

## ADDED Requirements

### Requirement: SQLite Database File Creation
Le système DOIT créer automatiquement le fichier de base de données SQLite lors du premier lancement de l'application.

#### Scenario: First application launch
- **WHEN** l'application démarre et qu'aucun fichier crm.db n'existe dans le dossier du projet
- **THEN** le système crée automatiquement le fichier crm.db

#### Scenario: Existing database file
- **WHEN** l'application démarre et que le fichier crm.db existe déjà
- **THEN** le système utilise la base existante sans la recréer

#### Scenario: Database file location
- **WHEN** le fichier crm.db est créé
- **THEN** le système le place à la racine du projet (même niveau que app.py)

### Requirement: Deals Table Schema
Le système DOIT créer une table deals avec toutes les colonnes définies dans le PRD.

#### Scenario: Table creation with all columns
- **WHEN** la base est initialisée
- **THEN** le système crée une table deals avec les colonnes: id (INTEGER PRIMARY KEY AUTOINCREMENT), client (TEXT NOT NULL), statut (TEXT NOT NULL), montant_brut (REAL NOT NULL), probabilite (REAL NOT NULL), valeur_ponderee (REAL NOT NULL), secteur (TEXT), date_echeance (DATE), assignee (TEXT), notes (TEXT)

#### Scenario: Primary key constraint
- **WHEN** un nouveau deal est inséré sans spécifier d'id
- **THEN** le système génère automatiquement un id unique auto-incrémenté

#### Scenario: NOT NULL constraints
- **WHEN** un INSERT tente d'insérer un deal sans client, statut ou montant_brut
- **THEN** la base rejette l'insertion avec erreur "NOT NULL constraint failed"

#### Scenario: Optional fields
- **WHEN** un deal est inséré sans secteur, date_echeance, assignee ou notes
- **THEN** le système accepte l'insertion et stocke NULL pour ces champs

### Requirement: SQL Schema File
Le système DOIT définir le schéma de création dans un fichier SQL séparé pour la maintenabilité.

#### Scenario: Schema file location
- **WHEN** le module database est chargé
- **THEN** le système lit le fichier database/init_schema.sql pour obtenir les commandes CREATE TABLE

#### Scenario: Idempotent schema initialization
- **WHEN** la fonction d'initialisation est appelée plusieurs fois
- **THEN** le système utilise CREATE TABLE IF NOT EXISTS pour éviter les erreurs si la table existe déjà

### Requirement: Database Connection Management
Le système DOIT fournir une fonction de connexion singleton pour éviter les connexions multiples.

#### Scenario: Singleton connection instance
- **WHEN** plusieurs modules appellent get_connection()
- **THEN** le système retourne toujours la même instance de connexion SQLite

#### Scenario: Connection reuse
- **WHEN** un module termine une opération database
- **THEN** le système garde la connexion ouverte pour réutilisation (pas de close après chaque query)

#### Scenario: Application shutdown
- **WHEN** l'application Streamlit se termine
- **THEN** le système ferme proprement la connexion database

### Requirement: Connection Module Structure
Le système DOIT organiser les fonctions database dans une structure modulaire claire.

#### Scenario: Connection module exports
- **WHEN** un composant importe database.connection
- **THEN** le système expose les fonctions get_connection() et init_database()

#### Scenario: Models module
- **WHEN** un module a besoin des définitions de colonnes
- **THEN** le système fournit database.models avec les constantes TABLE_NAME et COLUMNS

#### Scenario: CRUD module separation
- **WHEN** un module a besoin d'opérations database
- **THEN** le système fournit database.crud avec les fonctions insert_deals(), get_all_deals(), clear_all_deals()

### Requirement: Database Initialization on Startup
Le système DOIT initialiser automatiquement la base de données au démarrage de l'application.

#### Scenario: Automatic initialization in app.py
- **WHEN** app.py est exécuté avec streamlit run
- **THEN** le système appelle init_database() avant tout chargement de composants

#### Scenario: Silent initialization on success
- **WHEN** la base est initialisée avec succès
- **THEN** le système ne affiche aucun message (initialisation transparente)

#### Scenario: Initialization error display
- **WHEN** l'initialisation de la base échoue (permissions, espace disque, etc.)
- **THEN** le système affiche un message d'erreur Streamlit rouge et arrête l'application

### Requirement: SQLite Pragma Configuration
Le système DOIT configurer les pragmas SQLite appropriés pour optimiser les performances et l'intégrité.

#### Scenario: Foreign keys enforcement
- **WHEN** la connexion SQLite est établie
- **THEN** le système exécute PRAGMA foreign_keys = ON (préparation future relations)

#### Scenario: WAL mode for concurrency
- **WHEN** la connexion SQLite est établie
- **THEN** le système exécute PRAGMA journal_mode = WAL pour améliorer la performance des lectures/écritures

### Requirement: Data Type Mappings
Le système DOIT mapper correctement les types Python vers les types SQLite.

#### Scenario: String to TEXT mapping
- **WHEN** un champ Python str (client, statut, secteur, assignee, notes) est inséré
- **THEN** SQLite le stocke en type TEXT

#### Scenario: Float to REAL mapping
- **WHEN** un champ Python float (montant_brut, probabilite, valeur_ponderee) est inséré
- **THEN** SQLite le stocke en type REAL avec précision décimale

#### Scenario: Date to DATE mapping
- **WHEN** un champ Python date ou datetime (date_echeance) est inséré
- **THEN** SQLite le stocke en type DATE au format ISO 8601 (YYYY-MM-DD)

#### Scenario: NULL handling
- **WHEN** un champ optionnel Python est None
- **THEN** SQLite le stocke comme NULL

### Requirement: Schema Migration Preparation
Le système DOIT préparer l'architecture pour les futures migrations de schéma.

#### Scenario: Version tracking comment
- **WHEN** le fichier init_schema.sql est créé
- **THEN** le système inclut un commentaire "-- Schema version: 1.0 - Initial MVP" en en-tête

#### Scenario: Future column additions
- **WHEN** de nouvelles colonnes devront être ajoutées en Phase 2
- **THEN** l'architecture permet d'exécuter des ALTER TABLE sans recréer la table

### Requirement: Database File Exclusion from Git
Le système DOIT configurer .gitignore pour exclure le fichier database du versioning.

#### Scenario: Database file ignored
- **WHEN** git status est exécuté
- **THEN** le fichier crm.db n'apparaît pas dans les fichiers non trackés (présent dans .gitignore)

#### Scenario: Schema file versioned
- **WHEN** git status est exécuté
- **THEN** le fichier database/init_schema.sql est tracké et versionné
