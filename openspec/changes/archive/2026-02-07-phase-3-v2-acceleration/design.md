## Context

Le CRM Dashboard est une application Flask + HTML/JS/Tailwind + Chart.js déployée sur Vercel, avec Supabase PostgreSQL comme base de données (fallback SQLite). Les Phases 1 et 2 sont complétées : import CSV, KPIs, CRUD deals, filtres avancés, performance commerciale.

L'architecture actuelle suit un pattern API REST :
- **Backend** : Flask blueprints (`api/analytics.py`, `api/deals.py`, `api/upload.py`)
- **Business Logic** : `business_logic/calculators.py` pour les calculs métier
- **Frontend** : `templates/dashboard.html` avec appels `fetch()` vers les endpoints API
- **Graphiques** : Chart.js 4.4.0

La table `deals` possède déjà les champs `created_at` et `updated_at` (timestamps), ce qui permet de calculer la vélocité et détecter les deals froids sans migration de schéma.

## Goals / Non-Goals

**Goals :**
- Ajouter 3 nouvelles fonctionnalités d'accélération commerciale dans le dashboard existant
- Maintenir la cohérence architecturale (même pattern API REST + Chart.js)
- Aucune nouvelle dépendance externe
- Aucune modification du schéma de base de données

**Non-Goals :**
- Pas d'historique des transitions de statut (table dédiée) — la vélocité se base sur `created_at` → `updated_at` pour les deals "Gagné"
- Pas de notifications email (mentionnées dans ARCHITECTURE.md Phase 3, reportées)
- Pas de simulateur multi-variables — uniquement variation du panier moyen
- Pas de système de relance automatisé (envoi email/SMS) — uniquement marquage visuel

## Decisions

### 1. Calcul de la vitesse de vente via `created_at` → `updated_at`

**Choix** : Utiliser `updated_at - created_at` pour les deals au statut "Gagné" comme proxy de la durée de conversion.

**Alternatives considérées** :
- *Table d'historique des transitions* : Plus précis (Prospect → Qualifié → Négo → Gagné), mais nécessite une migration de schéma, un trigger d'audit et une refonte du CRUD. Surdimensionné pour le V2.
- *Champ `date_cloture` dédié* : Plus propre mais nécessite migration + MAJ du formulaire CRUD.

**Justification** : Le champ `updated_at` est automatiquement mis à jour lors du passage au statut "Gagné". C'est une approximation acceptable : si un deal est modifié après avoir été gagné (ex: correction de notes), le calcul sera biaisé, mais ce cas est rare pour un usage fondateur solo.

### 2. Simulateur What-If côté client

**Choix** : Calcul entièrement côté JavaScript à partir des données déjà chargées par l'endpoint `/api/kpis`.

**Alternatives considérées** :
- *Endpoint API dédié avec paramètre de variation* : Plus propre architecturalement, mais ajoute de la latence réseau pour chaque mouvement du curseur. L'interactivité temps réel serait dégradée.
- *WebSocket pour mise à jour en temps réel* : Surdimensionné pour un slider simple.

**Justification** : Les données nécessaires (pipeline pondéré, panier moyen, nombre de deals) sont déjà disponibles côté client après le chargement des KPIs. Un calcul JS local offre une réactivité instantanée du curseur sans appels réseau supplémentaires.

### 3. Détection des deals froids via un nouvel endpoint API

**Choix** : Créer un endpoint `GET /api/analytics/cold-deals` qui retourne les deals dont `updated_at < NOW() - 10 jours` et dont le statut n'est pas "Gagné".

**Alternatives considérées** :
- *Filtrage côté client* : Nécessite que `updated_at` soit inclus dans les données chargées. Actuellement, le dashboard ne récupère pas systématiquement ce champ pour l'affichage. Un endpoint dédié est plus propre.
- *Ajout dans l'endpoint KPIs existant* : Surchargerait le endpoint `/api/kpis` qui doit rester rapide et focalisé.

**Justification** : Un endpoint séparé respecte le pattern existant (un endpoint = une responsabilité). Le calcul SQL `WHERE updated_at < NOW() - INTERVAL '10 days'` est performant et exploite l'index existant.

### 4. Intégration dans le dashboard existant

**Choix** : Ajouter 3 nouvelles sections dans `dashboard.html`, après les sections existantes :
1. **Section "Vitesse de Vente"** : KPI + graphique barres (par commercial ou secteur)
2. **Section "Simulateur What-If"** : Curseur range HTML + affichage temps réel de la projection
3. **Section "Deals Froids"** : Badge compteur dans les KPIs + liste dédiée avec indicateurs visuels (badge rouge/orange)

**Justification** : Suit le pattern existant du dashboard (sections empilées, chacune alimentée par un fetch API). Pas de réorganisation nécessaire.

### 5. Nouvelles fonctions dans `calculators.py`

**Choix** : Ajouter dans `business_logic/calculators.py` :
- `calculate_sales_velocity(df)` → retourne la durée moyenne en jours pour les deals Gagné
- `calculate_velocity_by_group(df, group_col)` → ventilation par secteur ou commercial
- `get_cold_deals(df, threshold_days=10)` → retourne les deals inactifs

**Justification** : Maintient la séparation existante business_logic/api. Les fonctions sont testables unitairement.

## Risks / Trade-offs

- **Approximation vélocité** : Le calcul `updated_at - created_at` inclut les modifications post-conversion (édition de notes, etc.) → *Mitigation* : Acceptable pour usage solo, une table d'historique pourrait être ajoutée en Phase 4 si nécessaire.

- **Seuil de 10 jours fixe pour deals froids** : Peut ne pas convenir à tous les cycles de vente → *Mitigation* : Le seuil est défini comme constante dans `constants.py`, facilement modifiable. Un paramètre configurable pourrait être ajouté ultérieurement.

- **Simulateur limité à la variation du panier moyen** : Ne couvre pas d'autres scénarios (taux de conversion, volume de deals) → *Mitigation* : Le design permet d'étendre facilement le simulateur avec d'autres variables plus tard. Pour le V2, le panier moyen est le levier le plus actionnable pour le fondateur.

- **Compatibilité SQLite/PostgreSQL** : Les fonctions de date diffèrent entre les deux SGBD → *Mitigation* : Utiliser pandas pour les calculs de dates côté Python plutôt que des fonctions SQL spécifiques, comme le fait déjà l'endpoint deadlines.
