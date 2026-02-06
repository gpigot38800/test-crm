## Context

L'application CRM actuelle est construite avec Streamlit, ce qui a permis un prototypage rapide mais présente des limitations visuelles critiques : graphiques peu lisibles avec Plotly, noms de secteurs tronqués, et contrôle limité sur l'esthétique. Le fondateur a exprimé le besoin d'un rendu professionnel avec une meilleure modularité pour les évolutions futures.

**État actuel** :
- Architecture monolithe Streamlit (`app.py` + `components/`)
- Graphiques Plotly embarqués dans Streamlit
- Logique métier bien séparée (`database/`, `business_logic/`, `utils/`)
- Base SQLite fonctionnelle avec 22 deals démo
- MVP Phase 1 100% opérationnel (import CSV, KPIs, analyse secteur, échéances)

**Contraintes** :
- Conserver strictement le périmètre fonctionnel MVP Phase 1 (pas de nouvelles features)
- Réutiliser toute la logique métier existante sans modification
- Maintenir la compatibilité avec la base SQLite actuelle
- Interface claire et minimaliste (pas de mode sombre au MVP)
- Ne PAS exposer les clés API au client (selon CLAUDE.md)

**Parties prenantes** :
- Fondateur (utilisateur final solo)
- Déploiement local uniquement au MVP

## Goals / Non-Goals

**Goals:**
- Remplacer l'interface Streamlit par Flask + HTML/CSS/JS pour un contrôle total du design
- Améliorer significativement la lisibilité des graphiques avec Chart.js
- Créer une API REST propre pour séparer frontend/backend
- Conserver 100% de la logique métier existante (`database/`, `business_logic/`, `utils/`)
- Interface responsive (mobile-ready) avec Tailwind CSS
- Architecture modulaire facilitant les évolutions Phase 2+

**Non-Goals:**
- Ajouter de nouvelles fonctionnalités (saisie manuelle, filtres, authentification → Phase 2)
- Modifier la logique métier ou les calculs existants
- Migrer vers PostgreSQL (reste SQLite pour MVP)
- Conteneurisation Docker (déploiement local simple)
- Tests automatisés (Phase 2)
- Mode sombre (Phase 2)

## Decisions

### 1. Stack Frontend : Vanilla JS + Tailwind CSS (pas de framework React/Vue)

**Décision** : Utiliser HTML5 + Tailwind CSS (CDN) + Vanilla JavaScript

**Rationale** :
- **Simplicité** : Pas de build tools, pas de transpilation, développement direct
- **Rapidité** : Tailwind CSS via CDN = zéro configuration
- **Légèreté** : ~50KB gzippé vs 150KB+ pour React
- **Modularité** : Alpine.js peut être ajouté plus tard si besoin de réactivité
- **Contrôle** : Vanilla JS donne un contrôle total sur les interactions

**Alternatives considérées** :
- ❌ **React** : Overkill pour un dashboard solo, nécessite build tools (webpack/vite), courbe d'apprentissage
- ❌ **Vue.js** : Plus léger que React mais toujours un framework complet non nécessaire
- ✅ **Alpine.js** (futur) : Pourra être ajouté progressivement si besoin de réactivité côté client

### 2. Graphiques : Chart.js 4.x

**Décision** : Remplacer Plotly par Chart.js 4.4.0

**Rationale** :
- **Rendu supérieur** : Labels lisibles, animations fluides, design professionnel
- **Légèreté** : ~200KB vs 3MB+ pour Plotly
- **Personnalisation** : Contrôle total sur styles, couleurs, tooltips
- **Compatibilité** : Fonctionne parfaitement en vanilla JS
- **Documentation** : Excellente, nombreux exemples

**Alternatives considérées** :
- ❌ **Plotly.js** : Trop lourd, rendu actuel insatisfaisant
- ❌ **D3.js** : Trop bas niveau, temps de développement 3x supérieur
- ❌ **ApexCharts** : Bon rendu mais moins flexible que Chart.js

**Configuration Chart.js** :
- Barres horizontales pour secteurs (meilleure lisibilité des labels)
- Palette de couleurs cohérente (blues pour montants, greens pour paniers moyens)
- Tooltips personnalisés avec formatage € français
- Animations au scroll (entrance effects)

### 3. Architecture Backend : Flask avec Blueprint pattern

**Décision** : Application Flask avec blueprints pour organiser les routes API

**Structure** :
```
crm-dashboard/
├── app.py                    # Point d'entrée Flask
├── api/
│   ├── __init__.py          # Enregistrement blueprints
│   ├── deals.py             # Routes /api/deals/*
│   ├── analytics.py         # Routes /api/analytics/*
│   └── upload.py            # Routes /api/upload/*
├── templates/
│   ├── base.html            # Template de base
│   ├── dashboard.html       # Page principale
│   └── components/          # Partials réutilisables
│       ├── header.html
│       ├── kpi_cards.html
│       └── footer.html
├── static/
│   ├── css/
│   │   └── custom.css       # Styles personnalisés
│   ├── js/
│   │   ├── main.js          # Initialisation
│   │   ├── api.js           # Client API
│   │   ├── charts.js        # Configuration Chart.js
│   │   └── upload.js        # Upload CSV
│   └── img/
├── database/                 # CONSERVÉ tel quel
├── business_logic/           # CONSERVÉ tel quel
└── utils/                    # CONSERVÉ tel quel
```

**Rationale** :
- **Séparation claire** : API (/api/*) vs pages HTML (/)
- **Réutilisation** : Logique métier existante appelée par les blueprints
- **Évolutivité** : Facile d'ajouter de nouveaux blueprints Phase 2+
- **Testabilité** : Blueprints sont des modules Python testables

**Alternatives considérées** :
- ❌ **FastAPI** : Async non nécessaire pour usage solo, typage plus verbeux
- ❌ **Django** : Trop lourd, ORM non compatible avec logique existante
- ✅ **Flask** : Léger, flexible, compatible avec SQLAlchemy existant

### 4. API Design : REST JSON avec conventions

**Décision** : API REST retournant du JSON, pas de rendu côté serveur sauf page initiale

**Endpoints** :
```
GET  /                          → dashboard.html (page principale)
GET  /api/deals                 → Liste tous les deals
GET  /api/kpis                  → KPIs calculés (pipeline, panier moyen, etc.)
GET  /api/analytics/sectors    → Analyse par secteur
GET  /api/analytics/deadlines   → Échéances (retards + 30j)
POST /api/upload/csv            → Upload et traitement CSV
DELETE /api/deals               → Clear tous les deals (avant import)
```

**Format de réponse** :
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

**Rationale** :
- **SPA-like** : Chargement initial HTML, puis API JSON pour interactions
- **Cacheable** : Réponses GET peuvent être cachées côté client
- **Debuggable** : Testable avec curl/Postman
- **Évolutif** : API peut servir de base pour app mobile future

### 5. Upload CSV : FormData avec streaming

**Décision** : Upload multipart/form-data avec traitement streaming

**Flux** :
1. Frontend : `<input type="file">` + drag & drop zone
2. JavaScript : FormData API + fetch POST
3. Backend : Flask request.files, validation puis insertion batch
4. Réponse : Statistiques d'import (nb deals, erreurs)
5. Frontend : Rafraîchissement automatique du dashboard

**Rationale** :
- **UX** : Drag & drop moderne vs widget Streamlit basique
- **Feedback** : Progress bar + messages d'erreur clairs
- **Performance** : Traitement batch conservé (insertion SQLite rapide)

### 6. Gestion d'État : Pas de state management complexe

**Décision** : Pas de Redux/Vuex, state local en JavaScript

**Rationale** :
- **Simplicité** : Dashboard lecture seule (sauf upload), peu d'interactions
- **Rechargement** : Après upload, simple appel API pour rafraîchir
- **Future** : Si besoin Phase 2+, Alpine.js peut gérer réactivité

### 7. Styling : Tailwind CSS via CDN + custom.css minimal

**Décision** : Tailwind CSS 3.x via CDN + fichier custom.css pour spécifiques

**Rationale** :
- **Pas de build** : CDN = zéro configuration
- **Utilitaire-first** : Classes directement dans HTML, rapide à prototyper
- **Responsive** : Breakpoints intégrés (sm:, md:, lg:)
- **Custom** : Fichier custom.css pour animations, Chart.js overrides

**Alternatives considérées** :
- ❌ **Tailwind avec build** : Overkill pour MVP, complexité inutile
- ❌ **Bootstrap** : Moins moderne, moins flexible
- ❌ **Pure CSS** : Temps de développement 3x supérieur

## Risks / Trade-offs

### [Risque] CDN Tailwind : Taille fichier (~3MB non optimisé)
**Mitigation** : Acceptable pour usage local solo. Si performance problématique Phase 2, migrer vers build avec purge CSS.

### [Risque] Vanilla JS : Maintenance si UI devient complexe Phase 2+
**Mitigation** : Architecture modulaire permet migration progressive vers Alpine.js ou framework si besoin.

### [Risque] Breaking change : Utilisateurs devront relancer l'app différemment
**Mitigation** : Documentation claire dans README. Commande reste simple : `python app.py` au lieu de `streamlit run app.py`.

### [Trade-off] Pas de hot-reload comme Streamlit
**Impact** : Développement moins fluide (redémarrage Flask manuel).
**Mitigation** : Flask debug mode avec auto-reload activé.

### [Trade-off] Plus de code frontend à maintenir vs Streamlit
**Impact** : HTML/JS/CSS à gérer vs composants Streamlit abstraits.
**Bénéfice** : Contrôle total, meilleure UX, architecture professionnelle.

## Migration Plan

### Phase 1 : Setup infrastructure (Jour 1 matin)
1. Créer nouvelle branche Git `migration-flask`
2. Installer dépendances : `pip install flask`
3. Créer structure dossiers (`api/`, `templates/`, `static/`)
4. Setup app.py Flask minimal avec route `/` servant dashboard.html

### Phase 2 : API Backend (Jour 1 après-midi)
1. Créer blueprints API (`api/deals.py`, `api/analytics.py`)
2. Implémenter endpoints GET (réutiliser logique existante)
3. Tester endpoints avec curl
4. Implémenter POST /api/upload/csv

### Phase 3 : Frontend Dashboard (Jour 2 matin)
1. Créer base.html avec Tailwind CSS CDN
2. Créer dashboard.html avec structure HTML
3. Implémenter KPI cards (4 métriques)
4. Intégrer Chart.js (CDN)

### Phase 4 : Graphiques Chart.js (Jour 2 après-midi)
1. Graphique secteurs (barres horizontales)
2. Graphique panier moyen (top 5)
3. Tableau récapitulatif secteurs
4. Tableaux échéances (retards + 30j)

### Phase 5 : Upload CSV (Jour 3 matin)
1. Interface upload avec drag & drop
2. Connexion API POST /api/upload/csv
3. Feedback utilisateur (success/errors)
4. Rafraîchissement automatique

### Phase 6 : Polish & Tests (Jour 3 après-midi)
1. Responsive design (mobile/tablet)
2. Animations et transitions
3. Tests manuels complets
4. Documentation README

### Rollback Strategy
- Conserver branche `main` avec Streamlit intacte
- Si problème, simple `git checkout main`
- Aucun changement base de données (SQLite compatible)

## Open Questions

1. **Faut-il conserver l'ancien code Streamlit ?**
   - Recommandation : Oui, dans un dossier `archive/streamlit-old/` pour référence

2. **Faut-il ajouter un loader/spinner pendant chargement données ?**
   - Recommandation : Oui, simple spinner CSS pendant appels API

3. **Exporter les graphiques en PNG/SVG ?**
   - Recommandation : Non au MVP, Chart.js le supporte mais c'est Phase 2
