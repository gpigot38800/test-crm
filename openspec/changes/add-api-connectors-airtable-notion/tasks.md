## 1. Setup et dépendances

- [x] 1.1 Ajouter requests dans requirements.txt (pyairtable/notion-client incompatibles Python 3.14)
- [x] 1.2 Créer le package connectors/ avec __init__.py, base.py, airtable.py, notion.py, field_mapping.py

## 2. Schéma base de données

- [x] 2.1 Ajouter CREATE TABLE IF NOT EXISTS connector_configs (id, provider UNIQUE, api_token, base_id, table_name, field_mapping, is_active, updated_at) dans database/connection.py init_database()
- [x] 2.2 Ajouter CREATE TABLE IF NOT EXISTS sync_logs (id, provider, direction, status, records_processed, records_created, records_updated, error_message, started_at, completed_at) dans database/connection.py init_database()
- [x] 2.3 Créer les fonctions CRUD pour connector_configs dans database/crud.py : get_connector_config(provider), upsert_connector_config(provider, data), get_all_connector_configs()
- [x] 2.4 Créer les fonctions CRUD pour sync_logs dans database/crud.py : insert_sync_log(data), get_sync_logs(limit, provider_filter)

## 3. Connecteur de base, mapping et normalisation des statuts

- [x] 3.1 Implémenter la classe abstraite BaseConnector dans connectors/base.py avec les méthodes : test_connection(), fetch_records(), push_records()
- [x] 3.2 Implémenter le module field_mapping.py avec le mapping par défaut, la conversion CRM→externe et externe→CRM, et la validation du mapping
- [x] 3.3 Ajouter un dictionnaire STATUS_NORMALIZATION_MAP dans utils/constants.py pour mapper les statuts anglais et variantes courantes vers les statuts français du CRM
- [x] 3.4 Implémenter la fonction normalize_status(statut) dans connectors/field_mapping.py
- [x] 3.5 Intégrer normalize_status() dans la logique d'import (api/sync.py) : statuts inconnus → "prospect" par défaut avec mention dans le résumé

## 4. Connecteur Airtable

- [x] 4.1 Implémenter AirtableConnector.test_connection() : authentification PAT via requests, vérification base_id et table_name, retour du nombre de records
- [x] 4.2 Implémenter AirtableConnector.fetch_records() : récupération via API REST avec pagination offset, conversion des champs vers format deal CRM
- [x] 4.3 Implémenter AirtableConnector.push_records() : récupération des records existants, identification par nom client, batch create/update (max 10 par requête)

## 5. Connecteur Notion

- [x] 5.1 Implémenter NotionConnector.test_connection() : authentification via requests + Notion-Version header, vérification database_id, retour du titre et nombre de pages
- [x] 5.2 Implémenter NotionConnector.fetch_records() : récupération via API REST avec pagination start_cursor, extraction des propriétés Notion (title, number, date, select, rich_text, status, multi_select, checkbox)
- [x] 5.3 Implémenter NotionConnector.push_records() : requête existante pour matcher par client, pages create/update via API REST, construction des propriétés Notion depuis les valeurs CRM

## 6. Logique de synchronisation

- [x] 6.1 Implémenter la logique d'import dans sync_import() : charger config, instancier connecteur, fetch_records, normaliser statuts, calculer probabilité/valeur_ponderee, matcher par client, insert_deal/update_deal
- [x] 6.2 Implémenter la logique d'export dans sync_export() : charger config, instancier connecteur, get_all_deals, push_records avec mapping
- [x] 6.3 Implémenter le logging de synchronisation : insert_sync_log à chaque opération avec started_at, completed_at, status, décomptes et error_message

## 7. Blueprint Flask API sync

- [x] 7.1 Créer api/sync.py avec le blueprint sync_bp et l'enregistrer dans api/__init__.py register_blueprints()
- [x] 7.2 Implémenter GET /api/connectors/config : retourne toutes les configs avec token masqué ("***")
- [x] 7.3 Implémenter PUT /api/connectors/config/<provider> : validation provider (airtable/notion), upsert config, gestion du cas "pas de token = conserver l'existant"
- [x] 7.4 Implémenter POST /api/connectors/test/<provider> : charger config, instancier connecteur, appeler test_connection(), retourner résultat
- [x] 7.5 Implémenter POST /api/sync/<provider>/import : appeler import_from_provider(), logger sync_log, retourner décompte
- [x] 7.6 Implémenter POST /api/sync/<provider>/export : appeler export_to_provider(), logger sync_log, retourner décompte
- [x] 7.7 Implémenter GET /api/sync/logs : retourner les 50 derniers logs avec filtrage optionnel par provider

## 8. Interface utilisateur - Page Connecteurs

- [x] 8.1 Ajouter la route Flask GET /connectors dans app.py qui sert le template connectors.html
- [x] 8.2 Ajouter le lien "Connecteurs" dans la navigation principale du dashboard (templates existants)
- [x] 8.3 Créer le template templates/connectors.html avec les onglets Airtable et Notion, formulaires de configuration (token password, base_id, table_name), section mapping des champs
- [x] 8.4 Implémenter le JS pour charger la config existante au chargement (GET /api/connectors/config), pré-remplir les formulaires, masquer le token
- [x] 8.5 Implémenter le JS pour sauvegarder la config (PUT /api/connectors/config/<provider>), gérer le cas token non modifié
- [x] 8.6 Implémenter le bouton "Tester la connexion" avec badge vert/rouge selon le résultat (POST /api/connectors/test/<provider>)
- [x] 8.7 Implémenter les boutons "Importer" et "Exporter" avec indicateur de chargement et affichage du résumé (X créés, Y mis à jour, Z erreurs), désactivation si config incomplète
- [x] 8.8 Implémenter le tableau des logs de synchronisation (GET /api/sync/logs) avec badges colorés (vert/rouge/orange) et message d'erreur au survol
- [x] 8.9 Assurer le responsive design de la page (mobile < 768px : onglets empilés, formulaires pleine largeur)

## 9. Tests et validation

- [ ] 9.1 Tester manuellement le flux complet Airtable : config → test connexion → import → vérification deals en base → export (requiert credentials réels)
- [ ] 9.2 Tester manuellement le flux complet Notion : config → test connexion → import → vérification deals en base → export (requiert credentials réels)
- [x] 9.3 Vérifier que les tokens ne sont jamais renvoyés au client (GET /api/connectors/config retourne "***") — validé via Playwright
- [x] 9.4 Vérifier le responsive de la page /connectors avec Playwright — validé desktop 1280px + mobile 375px
- [x] 9.5 Vérifier que les blueprints existants (deals, analytics, upload) fonctionnent toujours sans régression — validé, dashboard principal intact
- [ ] 9.6 Vérifier la normalisation des statuts : importer des deals avec statuts anglais (requiert credentials réels pour test end-to-end)
