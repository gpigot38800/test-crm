## Context

Le dashboard CRM est actuellement en Phase 1 (MVP), construit avec Flask + HTML/CSS/JS (vanilla) + SQLite. L'application expose des endpoints REST (`/api/deals`, `/api/kpis`, `/api/analytics/sectors`, `/api/analytics/deadlines`, `/api/upload/csv`) et un frontend responsive avec Tailwind CSS et Chart.js.

L'architecture est bien structurée en couches : `api/` (blueprints Flask), `database/` (connexion SQLite + CRUD), `business_logic/` (calculators, validators, filters), `utils/` (formatters, constants), `static/js/` (api, main, charts, upload) et `templates/` (base.html, dashboard.html).

Le passage en V1 (Phase 2) ajoute 3 capacités : saisie manuelle des deals (CRUD complet), performance commerciale par assignee, et filtres avancés appliqués globalement.

**Contraintes** :
- Pas de nouvelles dépendances (vanilla JS, Tailwind CDN, Chart.js CDN)
- Interface claire et minimaliste, pas de mode sombre
- Conserver la structure existante (blueprints, business_logic, database)
- SQLite uniquement (pas de migration vers PostgreSQL pour le moment)

## Goals / Non-Goals

**Goals :**
- Permettre la création, modification et suppression d'un deal individuel via un formulaire modal
- Afficher les métriques de performance par commercial (volume, taux de conversion, pipeline)
- Filtrer dynamiquement l'ensemble du dashboard (KPIs, graphiques, tableaux) via une sidebar
- Persister les filtres en `localStorage` pour conserver le contexte entre sessions
- Maintenir la responsivité (mobile-friendly) sur les nouvelles sections

**Non-Goals :**
- Pas d'authentification (reporté Phase 3)
- Pas d'export Excel/PDF (reporté Phase 2 ultérieure)
- Pas de recherche full-text avancée (la recherche textuelle sera un simple `LIKE` SQL)
- Pas de pagination côté serveur (volume de données < 1000 deals)
- Pas de drag & drop de réordonnancement des deals

## Decisions

### 1. Formulaire deal : Modal overlay plutôt que page dédiée

**Choix** : Modal HTML/JS superposé au dashboard, réutilisé pour création et édition.

**Alternatives considérées** :
- **Page dédiée `/deals/new`** : Nécessiterait du routing côté client ou des templates Flask supplémentaires. Rompt le flux de travail « tout-en-un-écran » du fondateur.
- **Formulaire inline dans le tableau** : Complexe à gérer avec les validations, peu lisible sur mobile.

**Justification** : Le fondateur travaille seul sur un écran. Un modal permet de rester dans le contexte du dashboard, d'ajouter/modifier un deal rapidement, puis de voir immédiatement les KPIs mis à jour. Un seul template `dashboard.html` reste le point d'entrée.

**Implémentation** :
- Le HTML du modal vit dans `dashboard.html` (structure Tailwind : backdrop + conteneur centré)
- Un fichier `static/js/deal-form.js` gère l'ouverture/fermeture, le pré-remplissage (édition), la validation côté client, et l'envoi via `api.js`
- Le modal est ouvert soit par un bouton « + Nouveau Deal », soit par un clic sur une ligne de deal existant
- Après soumission réussie, le modal se ferme et `refreshDashboard()` est appelé

### 2. CRUD API : Endpoints REST classiques sur le blueprint `deals`

**Choix** : Ajouter `POST /api/deals`, `PUT /api/deals/<id>`, `DELETE /api/deals/<id>` au blueprint `deals_bp` existant.

**Alternatives considérées** :
- **Nouveau blueprint `crud_bp`** : Fragmente inutilement les routes deals.
- **Endpoint unique `PATCH /api/deals`** : Moins standard, complique le frontend.

**Justification** : Le blueprint `deals_bp` dans `api/deals.py` gère déjà `GET` et `DELETE` (bulk). Ajouter les 3 routes manquantes garde la cohérence RESTful. Chaque route appelle `database/crud.py` qui est étendu avec `get_deal_by_id()`, `insert_deal()`, `update_deal()`, `delete_deal()`.

**Validation** : La validation serveur réutilise `business_logic/validators.py` avec une nouvelle fonction `validate_deal_dict(data: dict)` qui applique les mêmes règles que `validate_deal_row()` mais sur un dict (entrée formulaire). Les probabilités et valeurs pondérées sont auto-calculées via `calculators.py`.

### 3. Filtres : Sidebar collapsible avec query parameters API

**Choix** : Sidebar HTML à gauche du dashboard, envoyant les filtres comme query parameters aux endpoints API existants.

**Alternatives considérées** :
- **Filtrage côté client uniquement** : Charge tous les deals puis filtre en JS. Simple mais ne scale pas et duplique la logique.
- **Endpoint dédié `/api/deals/filtered`** : Duplique la logique de `GET /api/deals`.

**Justification** : Le filtrage côté serveur via query parameters est le pattern le plus standard. Les endpoints existants (`/api/deals`, `/api/kpis`, `/api/analytics/sectors`, `/api/analytics/deadlines`) sont modifiés pour accepter des paramètres optionnels : `statut`, `secteur`, `assignee`, `date_from`, `date_to`, `search`. Quand aucun paramètre n'est fourni, le comportement reste identique à l'existant (rétro-compatible).

**Implémentation backend** :
- Une fonction utilitaire `get_filtered_deals(params)` dans `database/crud.py` construit dynamiquement les clauses `WHERE` avec des paramètres liés (protection SQL injection via `?` placeholders SQLite)
- Tous les endpoints analytics appellent `get_filtered_deals()` au lieu de `get_all_deals()` lorsque des query params sont présents
- Les filtres sont extraits via `request.args` dans chaque route

**Implémentation frontend** :
- `static/js/filters.js` gère la sidebar : lecture des valeurs, construction de la query string, appel de `refreshDashboard(filters)`
- `api.js` est étendu pour passer les query params à chaque fonction fetch
- `localStorage` stocke les filtres actifs ; ils sont restaurés au chargement de la page
- Un bouton « Réinitialiser les filtres » vide le `localStorage` et recharge sans filtres

### 4. Performance commerciale : Section dédiée avec Chart.js bar chart

**Choix** : Nouvelle section dans `dashboard.html` entre les secteurs et les échéances, avec un graphique barres groupées (deals/taux) et un tableau récapitulatif.

**Alternatives considérées** :
- **Page séparée `/performance`** : Brise le flux « tout-en-un-écran ».
- **Intégration dans la section secteurs** : Mélange deux dimensions d'analyse différentes.

**Justification** : Le fondateur veut voir d'un coup d'oeil qui performe. Une section dédiée avec un chart barres groupées (nb deals + taux de conversion par assignee) + tableau (pipeline pondéré, panier moyen par commercial) donne l'info en 3 secondes.

**Implémentation** :
- Nouvel endpoint `GET /api/analytics/performance` dans `api/analytics.py`
- Calculs dans `business_logic/calculators.py` : `calculate_performance_by_assignee(df)` retourne volume, montant total, pipeline pondéré, taux de conversion par assignee
- `static/js/performance.js` : initialise le chart et le tableau
- Le chart utilise Chart.js barres verticales groupées (bleu = nb deals, vert = taux conversion)
- Données compatible avec les filtres (appelle `get_filtered_deals()`)

### 5. Tableau des deals : Ajout d'un tableau éditable

**Choix** : Ajouter une section « Liste des Deals » entre les KPIs et l'analyse secteurs, affichant tous les deals avec des boutons d'action (modifier, supprimer).

**Justification** : Pour éditer ou supprimer un deal, l'utilisateur a besoin de le voir. Le tableau sert de point d'entrée vers le modal d'édition. Chaque ligne affiche : client, statut (badge coloré), montant, secteur, assignee, date échéance, et des boutons action.

**Implémentation** :
- Nouvelle section dans `dashboard.html` avec un tableau responsive
- Bouton « Modifier » ouvre le modal pré-rempli avec les données du deal
- Bouton « Supprimer » affiche une confirmation puis appelle `DELETE /api/deals/<id>`
- Le tableau est rechargé à chaque `refreshDashboard()`
- Le tableau respecte les filtres actifs

### 6. Layout : Structure avec sidebar collapsible

**Choix** : Modifier `base.html` pour supporter un layout 2 colonnes (sidebar filtres + contenu principal) avec sidebar collapsible sur mobile.

**Implémentation** :
- Desktop : sidebar fixe à gauche (250px), contenu principal à droite
- Mobile : sidebar cachée par défaut, bouton hamburger dans le header pour la déplier (overlay)
- La sidebar contient : filtres multi-select (statuts, secteurs, commerciaux), date range, champ recherche, bouton réinitialiser
- Les multi-selects utilisent des checkboxes Tailwind stylisées (pas de librairie externe)

## Risks / Trade-offs

**[Complexité JS accrue]** : L'ajout de 3 fichiers JS (deal-form.js, filters.js, performance.js) augmente la surface de code frontend vanilla. → **Mitigation** : Chaque fichier a une responsabilité unique et les fonctions partagées restent dans `api.js` et `main.js`. On garde l'approche module-par-fichier existante.

**[Filtrage côté serveur avec SQLite]** : Les requêtes dynamiques avec `WHERE` multiples pourraient devenir lentes sur de gros volumes. → **Mitigation** : Le volume attendu est < 1000 deals. SQLite avec les index existants (statut, secteur, date_echeance, assignee) est largement suffisant.

**[Modal form sans librairie]** : La gestion du formulaire (validation, état, fermeture) en vanilla JS est plus verbeuse qu'avec un framework. → **Mitigation** : Le formulaire a 7 champs maximum, la validation HTML5 (`required`, `type="number"`, `type="date"`) réduit le code custom nécessaire. On utilise `reportValidity()` natif.

**[localStorage pour les filtres]** : Si l'utilisateur change de navigateur, ses filtres sont perdus. → **Mitigation** : Acceptable pour un usage solo. Un bouton « Réinitialiser » permet de repartir de zéro facilement.

**[Rétro-compatibilité API]** : Les endpoints existants changent de comportement quand des query params sont fournis. → **Mitigation** : Sans paramètres, le comportement est strictement identique (rétro-compatible). Les tests Playwright existants restent valides.
