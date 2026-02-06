## Context

Le dashboard CRM utilise Streamlit + SQLite pour un fondateur solo. L'architecture existante (définie dans ARCHITECTURE.md) prévoit une structure modulaire avec séparation database/business_logic/components. Ce changement implémente la première fonctionnalité du MVP : permettre l'import de données existantes et calculer le pipeline pondéré.

**État actuel** :
- Structure projet vide (pas encore de code)
- Base de données non initialisée
- Fichier CSV demo disponible : `crm_prospects_demo.csv`

**Contraintes** :
- SQLite (migration PostgreSQL prévue Phase 2)
- Streamlit pour l'UI
- Pas d'authentification au MVP
- Développement rapide (3 jours pour MVP)

## Goals / Non-Goals

**Goals:**
- Créer le schéma SQLite avec table `deals` et toutes ses colonnes
- Permettre l'upload d'un fichier CSV via interface Streamlit
- Parser et valider les données CSV (montants positifs, dates valides, statuts reconnus)
- Mapper automatiquement les colonnes CSV vers le schéma database
- Calculer automatiquement les probabilités selon les règles métier (Prospect=10%, Qualifié=30%, Négociation=70%, Gagné=100%)
- Calculer la valeur pondérée pour chaque deal (montant_brut × probabilite)
- Afficher le KPI "Pipeline Pondéré Total" (somme des valeurs pondérées)
- Permettre plusieurs imports successifs sans dupliquer les données

**Non-Goals:**
- Édition manuelle des deals (Phase 2)
- Export de données (Phase 2)
- Graphiques sectoriels (autre feature MVP)
- Gestion des échéances (autre feature MVP)
- Authentification ou multi-utilisateurs
- Migration PostgreSQL (future)

## Decisions

### 1. Architecture Database Layer

**Décision** : Structure modulaire `database/` avec séparation connection/models/crud/schema

**Rationale** :
- **Évolutivité** : Facilite migration SQLite → PostgreSQL en Phase 2 (seul `connection.py` à modifier)
- **Testabilité** : CRUD séparé permet tests unitaires sans Streamlit
- **Maintenabilité** : Séparation claire des responsabilités

**Alternatives considérées** :
- ❌ Requêtes SQL directes dans `app.py` : code spaghetti, difficulté tests, duplication
- ❌ ORM SQLAlchemy : overkill pour SQLite MVP, ajout complexité inutile (migration PostgreSQL utilisera SQLAlchemy)

**Fichiers** :
```
database/
├── __init__.py
├── connection.py       # Connexion SQLite singleton
├── models.py          # Définitions colonnes table deals
├── crud.py            # insert_deals(), get_all_deals(), clear_all_deals()
└── init_schema.sql    # CREATE TABLE deals
```

### 2. Parsing CSV avec Pandas

**Décision** : Utiliser `pandas.read_csv()` avec validation post-parsing

**Rationale** :
- **Robustesse** : Pandas gère encodages (UTF-8, Latin-1), délimiteurs variés, quotes
- **Performance** : Natif C, optimisé pour gros volumes
- **Intégration** : Déjà dépendance du projet, conversion DataFrame → dict triviale

**Alternatives considérées** :
- ❌ Module `csv` standard : nécessite gestion manuelle encodage, types, erreurs
- ❌ PapaParse (JS) : nécessiterait composant React (hors scope Streamlit)

**Pipeline** :
```python
df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
# Validation : check colonnes requises, types, valeurs
# Normalisation : strip whitespace, lowercase statuts
# Mapping : rename colonnes CSV → colonnes DB
# Insertion : df.to_dict('records') → crud.insert_deals()
```

### 3. Calcul des Probabilités

**Décision** : Mapping statique statut → probabilité dans `business_logic/calculators.py`

**Rationale** :
- **Simplicité** : Règles fixes définies dans PRD (pas de logique complexe)
- **Performance** : Lookup dict O(1)
- **Traçabilité** : Constantes explicites dans `utils/constants.py`

**Implémentation** :
```python
# utils/constants.py
PROBABILITY_MAP = {
    'prospect': 0.10,
    'qualifié': 0.30,
    'négociation': 0.70,
    'gagné': 1.00
}

# business_logic/calculators.py
def calculate_probability(statut: str) -> float:
    normalized = statut.lower().strip()
    return PROBABILITY_MAP.get(normalized, 0.10)  # default Prospect

def calculate_weighted_value(montant_brut: float, probabilite: float) -> float:
    return round(montant_brut * probabilite, 2)
```

**Gestion des statuts non reconnus** :
- Défaut à 0.10 (Prospect) + log warning
- Validation côté CSV uploader affiche erreur si statut invalide

### 4. Validation des Données CSV

**Décision** : Validation en deux passes (structure + business logic)

**Rationale** :
- **Expérience utilisateur** : Feedback immédiat avant insertion DB
- **Intégrité** : Évite données corrompues en base
- **Debugging** : Logs clairs pour correction CSV

**Validations implémentées** :
1. **Structure** (`validators.py` → `validate_csv_structure()`)
   - Colonnes requises présentes : `client`, `statut`, `montant_brut`
   - Types compatibles : montant numérique, date parsable
2. **Business Logic** (`validators.py` → `validate_deal_row()`)
   - `montant_brut > 0`
   - `statut` dans liste autorisée (case-insensitive)
   - `date_echeance` au format ISO ou DD/MM/YYYY (si présente)
   - `client` non vide

**Stratégie d'erreur** :
- Erreur bloquante (structure) → arrêt import, message Streamlit rouge
- Warnings (lignes invalides) → skip ligne + log, affiche résumé (ex: "8/10 deals importés, 2 erreurs")

### 5. Gestion des Doublons

**Décision** : TRUNCATE table avant chaque import (Phase MVP)

**Rationale** :
- **Simplicité** : Évite logique de déduplication complexe
- **Usage MVP** : Fondateur solo, imports peu fréquents
- **Prévisibilité** : État DB = dernier CSV importé

**Implémentation** :
```python
# database/crud.py
def clear_all_deals(conn):
    conn.execute("DELETE FROM deals")
    conn.commit()

# components/csv_uploader.py
if st.button("Importer CSV"):
    clear_all_deals(get_connection())  # Nettoie avant import
    insert_deals(validated_data)
```

**Migration Phase 2** :
- Remplacer par logique UPSERT (UPDATE si `client` existe, INSERT sinon)
- Ou ajout colonne `import_id` pour traçabilité

### 6. Affichage KPI Pipeline Pondéré

**Décision** : Composant Streamlit `st.metric()` avec calcul temps réel

**Rationale** :
- **Simplicité** : Widget Streamlit natif, responsive
- **Performance** : Calcul en Python (sum en mémoire) vs query SQL (overhead)
- **Flexibilité** : Facile à étendre avec delta/comparaison périodes

**Implémentation** :
```python
# components/kpi_cards.py
def display_pipeline_kpi(deals_df):
    total_weighted = deals_df['valeur_ponderee'].sum()
    st.metric(
        label="Pipeline Pondéré Total",
        value=f"{total_weighted:,.0f} €",
        help="Somme des valeurs pondérées (montant × probabilité)"
    )
```

**Alternatives considérées** :
- ❌ Calcul SQL (`SELECT SUM(valeur_ponderee)`) : overhead connexion, moins flexible pour filtres futurs
- ❌ Graphique Plotly : overkill pour une métrique simple

## Risks / Trade-offs

### 1. SQLite en Production
**Risque** : Limite 1 writer → problème si multi-users en Phase 2
**Mitigation** : Migration PostgreSQL prévue Phase 2 (architecture modulaire facilite transition)

### 2. TRUNCATE avant Import
**Risque** : Perte de modifications manuelles futures (Phase 2 avec saisie manuelle)
**Mitigation** : Warning UX affiché avant import + migration UPSERT lors ajout saisie manuelle

### 3. Validation Stricte CSV
**Risque** : Rejet de fichiers légèrement non-conformes (frustration utilisateur)
**Mitigation** : Messages d'erreur explicites avec instructions correction + logs détaillés des lignes rejetées

### 4. Encodage CSV
**Risque** : Caractères spéciaux français (é, è, à) mal interprétés
**Mitigation** : `pd.read_csv(encoding='utf-8-sig')` + fallback `latin-1` en cas d'erreur

### 5. Performance Import Gros Fichiers
**Risque** : > 10k lignes → freeze UI Streamlit
**Mitigation** : Phase MVP limite 1k lignes + progress bar Streamlit + future async processing (Phase 3)

### 6. Dates Multiformats
**Risque** : CSV avec dates mixées (ISO, DD/MM/YYYY, MM/DD/YYYY)
**Mitigation** : Parser `dateutil.parser.parse()` avec `dayfirst=True` (Europe) + validation erreur

## Migration Plan

**Phase 1 - Initialisation (ce changement)** :
1. Créer structure `database/` avec modules
2. Exécuter `init_schema.sql` au premier lancement app
3. Implémenter CSV uploader + validators
4. Implémenter calculators + KPI card
5. Intégrer dans `app.py`

**Tests manuels** :
- Import `crm_prospects_demo.csv` → vérifier 10 deals insérés
- Vérifier calculs : deal "Prospect 50k€" → probabilite=0.10, valeur_ponderee=5000€
- Vérifier KPI affiché correspond à somme manuelle

**Rollback** :
- Supprimer fichier `crm.db` pour réinitialiser
- Pas de migration DB nécessaire (première version)

## Open Questions

**Q1** : Format exact des colonnes CSV demo ?
**A** : À valider lors implémentation avec fichier réel. Assumer headers: `Client, Statut, Montant, Tags, Date Échéance, Assignee, Notes`

**Q2** : Comportement si CSV contient deals avec même client mais montants différents ?
**A** : Phase MVP = TRUNCATE donc pas de collision. Phase 2 : ajouter colonne `deal_id` unique

**Q3** : Afficher historique des imports ?
**A** : Non-Goal Phase MVP. Future : ajouter table `import_logs` avec timestamp/filename/nb_rows
