## Why

Le MVP (Phase 1) est opérationnel avec l'import CSV, les KPIs flash, l'analyse sectorielle et la gestion des échéances. Cependant, le fondateur doit actuellement ré-importer un CSV complet pour modifier un seul deal, ne dispose d'aucune visibilité sur la performance de ses commerciaux, et ne peut pas filtrer dynamiquement les données affichées. Le passage en V1 (Phase 2) est nécessaire pour transformer le dashboard de consultation en véritable outil de pilotage quotidien.

## What Changes

- **Saisie manuelle des deals** : Formulaire modal pour créer, modifier et supprimer un deal individuel sans passer par l'import CSV. Ajout des endpoints REST `POST /api/deals`, `PUT /api/deals/<id>`, `DELETE /api/deals/<id>` et des opérations CRUD correspondantes en base.
- **Performance commerciale** : Nouveau panneau d'analyse affichant le volume de deals, le taux de succès et le pipeline pondéré par commercial (assignee). Ajout de l'endpoint `GET /api/analytics/performance`.
- **Filtres avancés** : Sidebar de filtrage avec multi-sélection par statut, secteur et commercial, plage de dates, et recherche textuelle. Les filtres s'appliquent à l'ensemble du dashboard (KPIs, graphiques, tableaux). Persistance des filtres via `localStorage`.

## Capabilities

### New Capabilities
- `deal-crud-form` : Formulaire modal HTML/JS pour créer, modifier et supprimer un deal individuellement, avec validation côté client et serveur.
- `commercial-performance` : Panneau d'analyse et endpoint API pour visualiser la performance par commercial (volume, taux de conversion, pipeline pondéré).
- `advanced-filters` : Sidebar de filtres dynamiques (statut, secteur, commercial, dates, recherche texte) appliqués globalement au dashboard avec persistance localStorage.

### Modified Capabilities
- `flask-api-backend` : Ajout des routes CRUD individuelles (`POST /api/deals`, `PUT /api/deals/<id>`, `DELETE /api/deals/<id>`) et du endpoint performance (`GET /api/analytics/performance`). Ajout du support des query parameters de filtrage sur les endpoints existants.
- `html-responsive-ui` : Ajout du layout pour le formulaire modal, la sidebar de filtres et la section performance commerciale dans le template dashboard.

## Impact

- **Backend** : `api/deals.py` (nouvelles routes CRUD), `api/analytics.py` (endpoint performance), `database/crud.py` (opérations update/delete/get_by_id, requêtes filtrées), `business_logic/calculators.py` (calculs performance par assignee), `business_logic/validators.py` (validation formulaire deal).
- **Frontend** : `templates/dashboard.html` (modal formulaire, sidebar filtres, section performance), nouveaux fichiers JS (`static/js/deal-form.js`, `static/js/filters.js`, `static/js/performance.js`), `static/js/api.js` (nouvelles fonctions fetch), `static/js/main.js` (intégration filtres globaux), `static/css/custom.css` (styles modal, sidebar, section performance).
- **Base de données** : Pas de changement de schéma (la table `deals` supporte déjà toutes les colonnes nécessaires). Ajout de requêtes avec clauses `WHERE` dynamiques.
- **Dépendances** : Aucune nouvelle dépendance. Utilisation des composants existants (Tailwind, Chart.js, vanilla JS).
