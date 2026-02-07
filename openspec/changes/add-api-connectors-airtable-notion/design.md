## Context

Le CRM est une application Flask monolithique avec :
- Un backend Python (Flask + blueprints API sous `/api/`)
- Un frontend HTML/JS servi par Flask (templates + static)
- Une base de données PostgreSQL/SQLite via `database/connection.py` (singleton)
- Des opérations CRUD existantes dans `database/crud.py` (insert_deal, update_deal, delete_deal, get_all_deals, etc.)
- Un système de blueprints API : `api/deals.py`, `api/analytics.py`, `api/upload.py`

L'objectif est d'ajouter des connecteurs Airtable et Notion pour synchroniser les deals bidirectionnellement, sans perturber l'architecture existante.

## Goals / Non-Goals

**Goals:**
- Permettre l'import de deals depuis Airtable et Notion vers le CRM
- Permettre l'export/push de deals du CRM vers Airtable et Notion
- Fournir une interface de configuration pour les tokens API, le choix des bases/tables, et le mapping des champs
- Logger toutes les opérations de synchronisation pour traçabilité
- Stocker les tokens côté serveur uniquement (jamais exposés au client)

**Non-Goals:**
- Synchronisation temps réel / webhooks (hors périmètre, sync manuelle uniquement)
- Sync automatique périodique (pas de scheduler/cron)
- Support d'autres plateformes que Airtable et Notion
- Résolution avancée de conflits (on applique "dernière écriture gagne")
- Migration des données existantes entre connecteurs

## Decisions

### 1. Architecture modulaire : dossier `connectors/`

**Choix** : Créer un package `connectors/` avec un module par service et une classe de base abstraite.

```
connectors/
├── __init__.py
├── base.py            # Classe abstraite BaseConnector
├── airtable.py        # AirtableConnector(BaseConnector)
├── notion.py          # NotionConnector(BaseConnector)
└── field_mapping.py   # Logique de mapping champs CRM ↔ service externe
```

**Pourquoi** : L'interface commune (`BaseConnector`) impose un contrat (fetch_records, push_records, test_connection) et facilite l'ajout futur d'autres connecteurs. Chaque module reste indépendant et testable.

**Alternative rejetée** : Tout mettre dans un seul fichier `sync.py`. Rejeté car les APIs Airtable et Notion sont très différentes (structure des réponses, types de champs) et un fichier unique deviendrait vite trop gros.

### 2. SDKs officiels Python

**Choix** : `pyairtable` pour Airtable, `notion-client` pour Notion.

- **pyairtable** : SDK officiel, gère le rate limiting (5 QPS) automatiquement avec retry, API simple (table.all(), table.create(), table.batch_create())
- **notion-client** : SDK officiel, gère le rate limiting (3 RPS) avec backoff exponentiel, supporte sync et async

**Pourquoi** : Les SDKs officiels gèrent automatiquement le rate limiting, la pagination et les erreurs réseau. Pas besoin de réinventer ces mécanismes.

**Alternative rejetée** : Appels HTTP directs avec `requests`. Plus de contrôle mais beaucoup plus de code boilerplate (pagination, retry, rate limiting) à maintenir.

### 3. Nouveau blueprint Flask `api/sync.py`

**Choix** : Un seul blueprint `sync_bp` avec tous les endpoints de synchronisation et de configuration.

Endpoints :
- `GET /api/connectors/config` — Récupérer la config des connecteurs (sans tokens)
- `PUT /api/connectors/config/<provider>` — Sauvegarder la config d'un connecteur
- `POST /api/connectors/test/<provider>` — Tester la connexion à un service
- `POST /api/sync/<provider>/import` — Importer les deals depuis le service vers le CRM
- `POST /api/sync/<provider>/export` — Exporter les deals du CRM vers le service
- `GET /api/sync/logs` — Historique des synchronisations

Où `<provider>` est `airtable` ou `notion`.

**Pourquoi** : Un seul blueprint cohérent plutôt que de polluer les blueprints existants. Le pattern `<provider>` évite la duplication d'endpoints.

### 4. Stockage de la configuration en base de données

**Choix** : Deux nouvelles tables SQL.

**Table `connector_configs`** :
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto-incrémenté |
| provider | TEXT UNIQUE | 'airtable' ou 'notion' |
| api_token | TEXT | Token chiffré ou en clair (usage solo) |
| base_id | TEXT | ID de la base Airtable ou database Notion |
| table_name | TEXT | Nom de la table source |
| field_mapping | TEXT (JSON) | Mapping champs service → CRM |
| is_active | BOOLEAN | Connecteur activé/désactivé |
| updated_at | TIMESTAMP | Dernière modification |

**Table `sync_logs`** :
| Colonne | Type | Description |
|---------|------|-------------|
| id | INTEGER PK | Auto-incrémenté |
| provider | TEXT | 'airtable' ou 'notion' |
| direction | TEXT | 'import' ou 'export' |
| status | TEXT | 'success', 'error', 'partial' |
| records_processed | INTEGER | Nombre de records traités |
| records_created | INTEGER | Nombre de records créés |
| records_updated | INTEGER | Nombre de records mis à jour |
| error_message | TEXT | Message d'erreur si applicable |
| started_at | TIMESTAMP | Début de la sync |
| completed_at | TIMESTAMP | Fin de la sync |

**Pourquoi** : La configuration persiste entre les redémarrages de l'app. Les logs permettent au fondateur de vérifier l'historique des syncs. Le token est stocké en base plutôt qu'en variable d'environnement pour permettre la configuration via l'UI.

**Alternative rejetée** : Stocker en variables d'environnement uniquement. Rejeté car ne permet pas la configuration via l'interface et nécessite un redémarrage pour changer les tokens.

### 5. Mapping de champs configurable

**Choix** : Mapping stocké en JSON dans `connector_configs.field_mapping` avec un mapping par défaut intelligent.

Mapping par défaut Airtable :
```json
{
  "client": "Name",
  "statut": "Status",
  "montant_brut": "Amount",
  "secteur": "Sector",
  "date_echeance": "Due Date",
  "assignee": "Assignee",
  "notes": "Notes"
}
```

Mapping par défaut Notion :
```json
{
  "client": "Name",
  "statut": "Status",
  "montant_brut": "Amount",
  "secteur": "Sector",
  "date_echeance": "Due Date",
  "assignee": "Assignee",
  "notes": "Notes"
}
```

L'utilisateur peut modifier le mapping via l'UI si ses colonnes ont des noms différents.

**Pourquoi** : Chaque utilisateur peut avoir des noms de colonnes différents dans Airtable/Notion. Le mapping par défaut couvre le cas courant (colonnes en anglais) tout en offrant la flexibilité de personnalisation.

### 6. Stratégie de synchronisation : identification par `client`

**Choix** : Lors de l'import, on identifie les deals existants par le champ `client` (nom du prospect). Si un deal avec le même client existe déjà, on met à jour. Sinon, on crée.

Lors de l'export, on pousse tous les deals du CRM vers le service. Si un record avec le même nom existe, on met à jour. Sinon, on crée.

**Pourquoi** : Le CRM n'a pas d'ID externe (pas de champ `airtable_id` ou `notion_page_id`). Le nom du client est le seul identifiant naturel partagé. Stratégie simple, suffisante pour un usage fondateur.

**Limitation connue** : Deux deals avec le même client ne seront pas distingués. Acceptable pour le MVP.

### 7. Sécurité des tokens API

**Choix** : Les tokens sont stockés en base de données. L'endpoint `GET /api/connectors/config` retourne la config **sans** le token (remplacé par `"***"` si configuré). Le token n'est jamais renvoyé au frontend.

**Pourquoi** : Conformité avec la contrainte CLAUDE.md "NE JAMAIS exposer les clés API au client". Le token ne transite vers le serveur que lors de la sauvegarde (PUT), jamais dans l'autre sens.

### 8. Page UI dédiée dans le frontend

**Choix** : Nouvelle page `/connectors` accessible depuis la navigation principale. Contient :
- Un onglet par connecteur (Airtable / Notion)
- Formulaire de configuration : token, base ID, table, mapping
- Bouton "Tester la connexion"
- Boutons "Importer" et "Exporter"
- Tableau des derniers logs de synchronisation

**Pourquoi** : Séparer la configuration des connecteurs du dashboard principal pour garder une interface claire et ne pas surcharger la page existante.

## Risks / Trade-offs

**[Rate limiting API externes]** → Les SDKs pyairtable et notion-client gèrent automatiquement les retries. Pour les gros volumes (>1000 records), l'opération peut prendre plusieurs secondes. On affiche un indicateur de progression côté UI.

**[Tokens stockés en clair en DB]** → Pour le MVP (usage solo, pas d'accès multi-utilisateurs), le risque est acceptable. En Phase 4 (multi-users), on devra chiffrer les tokens avec une clé applicative. Pour l'instant, la DB n'est pas exposée sur internet.

**[Matching par nom de client]** → Peut créer des doublons si deux deals ont le même client mais des montants différents. Mitigation : lors de l'import, afficher un résumé avant confirmation (records à créer vs à mettre à jour).

**[Dépendances supplémentaires]** → `pyairtable` (~2MB) et `notion-client` (~500KB) ajoutent de la taille. Impact négligeable.

**[Pas de sync temps réel]** → Le fondateur doit manuellement déclencher les syncs. Acceptable pour le MVP, webhook à prévoir en Phase 4.

## Open Questions

- Faut-il prévoir un mode "dry-run" qui montre les changements avant de les appliquer ? (Recommandé mais optionnel pour le MVP)
- Le mapping par défaut doit-il être en français (Nom, Statut, Montant) ou en anglais (Name, Status, Amount) ? (Dépend de la langue des bases Airtable/Notion du fondateur)
