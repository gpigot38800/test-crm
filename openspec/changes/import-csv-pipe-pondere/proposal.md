## Why

Le fondateur a besoin d'importer rapidement les données prospects depuis un fichier CSV existant (`crm_prospects_demo.csv`) et de visualiser immédiatement le pipeline pondéré pour prévoir le CA réel. Sans cette fonctionnalité, impossible de démarrer l'utilisation du dashboard CRM et d'exploiter les données existantes.

## What Changes

- **Import CSV automatisé** : Upload du fichier `crm_prospects_demo.csv` avec parsing, validation et insertion en base de données
- **Calcul automatique des probabilités** : Application des probabilités selon le statut (10% Prospect, 30% Qualifié, 70% Négociation, 100% Gagné)
- **Calcul de la valeur pondérée** : Pour chaque deal, `valeur_ponderee = montant_brut × probabilite`
- **Indicateur Pipeline Pondéré** : Somme totale des valeurs pondérées affichée en KPI principal pour prévoir le CA réel
- **Mapping colonnes CSV vers schéma DB** : Conversion automatique des colonnes CSV vers les champs de la table `deals`

## Capabilities

### New Capabilities

- `csv-import`: Gestion de l'upload, parsing et validation du fichier CSV avec mapping automatique vers le schéma database
- `weighted-pipeline-calculator`: Calcul des probabilités par statut, calcul des valeurs pondérées et affichage du pipeline pondéré total
- `database-initialization`: Création du schéma SQLite avec table `deals` et colonnes requises

### Modified Capabilities

<!-- Aucune capability existante n'est modifiée - c'est le MVP initial -->

## Impact

**Code affecté** :
- Création de `database/` : modules de connexion, modèles, CRUD, schéma SQL
- Création de `components/csv_uploader.py` : Interface upload CSV Streamlit
- Création de `business_logic/calculators.py` : Logique de calcul des probabilités et pondérations
- Création de `components/kpi_cards.py` : Affichage du KPI Pipeline Pondéré
- Fichier principal `app.py` : Intégration des composants

**Dépendances** :
- Pandas (parsing CSV)
- SQLite3 (base de données)
- Streamlit (interface)

**Base de données** :
- Création de la table `deals` avec colonnes : `id`, `client`, `statut`, `montant_brut`, `probabilite`, `valeur_ponderee`, `secteur`, `date_echeance`, `assignee`, `notes`
