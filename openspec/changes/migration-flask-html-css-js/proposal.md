## Why

Le rendu Streamlit actuel présente des limitations visuelles critiques pour un dashboard décisionnel : graphiques peu lisibles, noms de secteurs d'activité peu visibles, et manque de contrôle sur l'esthétique. Une migration vers Flask + HTML/CSS/JS permettra un contrôle pixel-perfect du design, des graphiques professionnels avec Chart.js, et une modularité maximale pour les évolutions futures, tout en conservant le même périmètre fonctionnel MVP Phase 1.

## What Changes

- **BREAKING**: Remplacement complet de l'interface Streamlit par une application Flask + HTML/CSS/JS
- Création d'une API REST Flask pour exposer les données (remplace les appels directs Streamlit)
- Nouveaux templates HTML avec Tailwind CSS pour l'interface utilisateur
- Migration des graphiques Plotly vers Chart.js pour un meilleur rendu visuel
- Conservation de toute la logique métier existante (database/, business_logic/, utils/)
- Maintien strict du périmètre fonctionnel MVP Phase 1 (aucune nouvelle fonctionnalité)

## Capabilities

### New Capabilities
- `flask-api-backend`: API REST Flask exposant les endpoints pour deals, KPIs et analytics
- `html-responsive-ui`: Interface HTML/CSS responsive avec Tailwind CSS pour le dashboard
- `chartjs-visualizations`: Graphiques interactifs Chart.js pour secteurs et pipeline
- `csv-upload-web`: Interface web d'upload CSV remplaçant le widget Streamlit

### Modified Capabilities
- `csv-import-processor`: Adapter l'import CSV pour fonctionner avec Flask (endpoint POST au lieu de widget)
- `kpi-calculator`: Exposer les KPIs via API REST au lieu de composants Streamlit
- `sector-analysis`: Refactoriser pour API REST et Chart.js au lieu de Plotly/Streamlit
- `deadline-management`: Refactoriser pour API REST et tableaux HTML au lieu de dataframes Streamlit

## Impact

**Code affecté** :
- `crm-dashboard/app.py` : Remplacé par application Flask avec routes API
- `crm-dashboard/components/` : Remplacé par templates HTML et endpoints API
- `crm-dashboard/requirements.txt` : Ajout Flask, suppression Streamlit/Plotly

**Code conservé** (aucune modification) :
- `crm-dashboard/database/` : Logique de connexion et CRUD conservée à l'identique
- `crm-dashboard/business_logic/` : Calculs et validations conservés à l'identique
- `crm-dashboard/utils/` : Formateurs et constantes conservés à l'identique

**Dépendances** :
- Ajout : Flask 3.0, Jinja2 (templates), Tailwind CSS (CDN)
- Suppression : Streamlit, Plotly
- Conservation : pandas, python-dateutil, SQLite

**Périmètre fonctionnel** : Strictement identique au MVP Phase 1 actuel
- ✅ Import CSV
- ✅ Pipeline pondéré total
- ✅ KPIs Flash (4 métriques)
- ✅ Analyse par Secteur (graphiques + tableau)
- ✅ Gestion des Échéances (retards + 30 jours)
- ✅ Aperçu des deals (tableau complet)

**Hors périmètre** : Toutes fonctionnalités Phase 2+ (saisie manuelle, filtres avancés, authentification, etc.)
