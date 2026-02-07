## Why

Le CRM fonctionne actuellement en silo : les données ne sont accessibles que via l'interface web et l'import CSV. Or, de nombreux fondateurs utilisent déjà Airtable et Notion comme outils de travail quotidiens pour gérer leurs prospects, notes de réunion et pipelines. L'absence de connecteurs API oblige à des double-saisies manuelles et crée des risques de désynchronisation entre les outils. Cette fonctionnalité, initialement repoussée dans la section "+ TARD" du PRD (Connecteurs API), est désormais prioritaire pour fluidifier le workflow du fondateur.

## What Changes

- **Nouveau connecteur Airtable** : synchronisation bidirectionnelle des deals entre le CRM et une base Airtable configurable. Import depuis Airtable vers le CRM et export/push du CRM vers Airtable.
- **Nouveau connecteur Notion** : synchronisation bidirectionnelle des deals entre le CRM et une base de données Notion. Import depuis Notion vers le CRM et export/push du CRM vers Notion.
- **Interface de configuration des connecteurs** : page dédiée dans l'UI pour configurer les clés API, sélectionner les bases/tables sources, et mapper les champs.
- **Synchronisation manuelle** : boutons pour déclencher import/export à la demande (pas de sync automatique en temps réel pour le MVP des connecteurs).
- **Gestion des conflits** : stratégie simple "dernière écriture gagne" avec log des actions de synchronisation.

## Capabilities

### New Capabilities
- `airtable-connector` : Connecteur API Airtable pour synchroniser les deals (import/export) entre une base Airtable et le CRM. Gestion de l'authentification par Personal Access Token, mapping des champs, et opérations CRUD via l'API REST Airtable.
- `notion-connector` : Connecteur API Notion pour synchroniser les deals (import/export) entre une base de données Notion et le CRM. Gestion de l'authentification par integration token, mapping des propriétés Notion vers les champs CRM, et opérations CRUD via l'API Notion.
- `connector-config-ui` : Interface utilisateur pour configurer, tester et déclencher les connecteurs API. Formulaires de configuration des tokens, sélection des bases/tables, mapping visuel des champs, et boutons de synchronisation.

### Modified Capabilities
- `flask-api-backend` : Ajout de nouveaux endpoints API pour les opérations de synchronisation (/api/sync/airtable, /api/sync/notion) et la configuration des connecteurs (/api/connectors/config).

## Impact

- **Code** : Nouveaux modules `connectors/airtable.py` et `connectors/notion.py`. Nouveaux endpoints Flask dans un blueprint `sync`. Nouvelle page UI pour la configuration.
- **API** : Nouveaux endpoints REST : POST/GET /api/sync/airtable, POST/GET /api/sync/notion, GET/PUT /api/connectors/config.
- **Dépendances** : Ajout des bibliothèques `pyairtable` (SDK Airtable officiel) et `notion-client` (SDK Notion officiel pour Python).
- **Configuration** : Nouvelles variables d'environnement pour les tokens API (AIRTABLE_TOKEN, NOTION_TOKEN). Les clés ne seront jamais exposées côté client conformément aux contraintes du CLAUDE.md.
- **Base de données** : Nouvelle table `connector_configs` pour stocker la configuration des connecteurs (bases, mapping de champs) et table `sync_logs` pour l'historique des synchronisations.
