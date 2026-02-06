## 1. Setup Projet et Structure

- [x] 1.1 Créer l'arborescence des dossiers (database/, business_logic/, components/, utils/)
- [x] 1.2 Créer les fichiers __init__.py pour chaque module Python
- [x] 1.3 Créer le fichier requirements.txt avec les dépendances (streamlit, pandas, python-dateutil)
- [x] 1.4 Mettre à jour .gitignore pour exclure crm.db et __pycache__

## 2. Database Layer - Schema et Connexion

- [x] 2.1 Créer database/init_schema.sql avec le CREATE TABLE deals (9 colonnes: id, client, statut, montant_brut, probabilite, valeur_ponderee, secteur, date_echeance, assignee, notes)
- [x] 2.2 Créer database/connection.py avec fonction get_connection() singleton et init_database()
- [x] 2.3 Configurer les pragmas SQLite (foreign_keys=ON, journal_mode=WAL) dans connection.py
- [x] 2.4 Créer database/models.py avec constantes TABLE_NAME et COLUMNS

## 3. Database Layer - Opérations CRUD

- [x] 3.1 Implémenter database/crud.py avec fonction insert_deals(deals_list) pour insertion batch
- [x] 3.2 Implémenter database/crud.py avec fonction get_all_deals() retournant DataFrame pandas
- [x] 3.3 Implémenter database/crud.py avec fonction clear_all_deals() pour TRUNCATE

## 4. Utils - Constantes et Formatters

- [x] 4.1 Créer utils/constants.py avec dictionnaire PROBABILITY_MAP (prospect:0.10, qualifié:0.30, négociation:0.70, gagné:1.00)
- [x] 4.2 Créer utils/constants.py avec liste VALID_STATUSES pour validation
- [x] 4.3 Créer utils/formatters.py avec fonction format_currency() pour affichage montants avec séparateurs de milliers

## 5. Business Logic - Calculateurs

- [x] 5.1 Créer business_logic/calculators.py avec fonction calculate_probability(statut) utilisant PROBABILITY_MAP
- [x] 5.2 Créer business_logic/calculators.py avec fonction calculate_weighted_value(montant_brut, probabilite) avec arrondi 2 décimales
- [x] 5.3 Créer business_logic/calculators.py avec fonction calculate_total_pipeline(deals_df) retournant somme valeurs_ponderees

## 6. Business Logic - Validateurs

- [x] 6.1 Créer business_logic/validators.py avec fonction validate_csv_structure(df) vérifiant colonnes requises
- [x] 6.2 Créer business_logic/validators.py avec fonction validate_deal_row(row) vérifiant montant>0, statut valide, client non vide
- [x] 6.3 Créer business_logic/validators.py avec fonction parse_date(date_str) supportant ISO et DD/MM/YYYY avec fallback
- [x] 6.4 Gérer les erreurs de validation avec retour de liste d'erreurs (ligne, champ, message)

## 7. Business Logic - Filtres

- [x] 7.1 Créer business_logic/filters.py avec fonction normalize_column_names(df) pour mapping case-insensitive
- [x] 7.2 Créer business_logic/filters.py avec fonction map_csv_to_schema(df) pour renommer colonnes CSV vers schéma DB

## 8. Components - CSV Uploader

- [x] 8.1 Créer components/csv_uploader.py avec interface st.file_uploader() acceptant uniquement .csv
- [x] 8.2 Implémenter parsing CSV avec pandas (encoding utf-8-sig, fallback latin-1)
- [x] 8.3 Intégrer validation structure et business logic avec affichage erreurs
- [x] 8.4 Ajouter barre de progression st.progress() pendant traitement (si >100 lignes)
- [x] 8.5 Implémenter appel clear_all_deals() avant insertion
- [x] 8.6 Calculer probabilite et valeur_ponderee pour chaque ligne valide
- [x] 8.7 Appeler insert_deals() avec données validées et calculées
- [x] 8.8 Afficher message succès vert ou rapport erreurs avec tableau récapitulatif

## 9. Components - KPI Pipeline Pondéré

- [x] 9.1 Créer components/kpi_cards.py avec fonction display_pipeline_kpi(deals_df)
- [x] 9.2 Utiliser st.metric() avec label "Pipeline Pondéré Total" et valeur formatée
- [x] 9.3 Ajouter help text "Somme des valeurs pondérées (montant × probabilité)"
- [x] 9.4 Gérer le cas table vide (afficher 0 €)

## 10. Intégration Application Principale

- [x] 10.1 Créer app.py avec import des modules nécessaires
- [x] 10.2 Appeler init_database() au démarrage avec gestion erreur
- [x] 10.3 Configurer page Streamlit (titre, layout wide)
- [x] 10.4 Afficher composant CSV uploader dans sidebar
- [x] 10.5 Charger deals avec get_all_deals() et stocker dans session_state
- [x] 10.6 Afficher KPI Pipeline Pondéré en haut de page
- [x] 10.7 Ajouter bouton refresh pour recharger données

## 11. Tests et Validation

- [ ] 11.1 Tester import du fichier crm_prospects_demo.csv (vérifier parsing)
- [ ] 11.2 Vérifier calculs probabilités pour chaque statut (Prospect=10%, Qualifié=30%, Négociation=70%, Gagné=100%)
- [ ] 11.3 Vérifier calculs valeurs pondérées (montant × probabilite avec 2 décimales)
- [ ] 11.4 Vérifier affichage Pipeline Pondéré Total (somme correcte)
- [ ] 11.5 Tester upload CSV avec erreurs (colonnes manquantes, montants invalides, statuts inconnus)
- [ ] 11.6 Vérifier rapport d'erreurs affiché correctement
- [ ] 11.7 Tester réimport CSV (vérifier TRUNCATE fonctionne)
- [ ] 11.8 Tester encodage UTF-8 et Latin-1 avec caractères accentués
