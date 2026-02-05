# 🏗️ Architecture Technique - Dashboard CRM

**Version** : 1.0
**Date** : 2025-02-05
**Statut** : MVP Phase 1

---

## 📋 Vue d'Ensemble

Dashboard CRM pour fondateur avec objectif de maximiser le volume et la valeur des deals, conçu pour évoluer vers un usage multi-utilisateurs dans 6-12 mois.

### Principes Directeurs
- ✅ **Rapidité de développement** : MVP en 3 jours
- ✅ **Simplicité architecturale** : Stack Python monolithique
- ✅ **Évolutivité préparée** : PostgreSQL dès le départ
- ✅ **Coûts maîtrisés** : Tiers gratuits pour démarrage

---

## 🎯 Stack Technique Retenue

### Frontend & Backend
- **Framework** : Streamlit 1.32+
- **Langage** : Python 3.11+
- **Architecture** : Monolithe (frontend + backend dans app.py)

**Justification** :
- Développement rapide (pure Python, pas de JS/HTML/CSS)
- Excellente intégration data science (Pandas, NumPy natifs)
- Adapté pour 1-50 utilisateurs
- Migration future possible vers React si nécessaire (> 100 users)

### Base de Données
- **SGBD** : PostgreSQL 15+
- **Hébergement** : Neon.tech (tier gratuit)
  - Limite : 10 GB storage
  - Serverless avec scaling automatique
  - Connection string : `postgresql://user:pass@host/dbname`
- **ORM** : SQLAlchemy 2.0+
- **Driver** : psycopg3

**Justification** :
- Multi-users ready (vs SQLite limité à 1 write)
- Scalabilité illimitée (tera-octets supportés)
- Évite migration database dans 6 mois
- Permissions granulaires natives (GRANT/REVOKE)
- Standard universel (portabilité garantie)

### Data Processing & Visualisation
- **Data manipulation** : Pandas 2.2+, NumPy 1.26+
- **Graphiques** : Plotly 5.18+ (interactivité)
- **CSV parsing** : Pandas `read_csv()` (natif)
- **Calculs métier** : Python pur (probabilités, pondérations)

### Déploiement
- **Phase MVP** : Local uniquement
  - Lancement : `streamlit run app.py`
  - Accès : `http://localhost:8501`
  - Pas de conteneur pour simplifier dev
- **Phase Production (future)** :
  - Docker + Railway/Render
  - Variables d'environnement (.env)
  - CI/CD GitHub Actions

---

## 📁 Structure Projet

```
crm-dashboard/
├── app.py                      # Point d'entrée Streamlit
├── requirements.txt            # Dépendances Python
├── .env.example               # Template variables environnement
├── .gitignore                 # Exclure .env, __pycache__, etc.
│
├── database/
│   ├── __init__.py
│   ├── connection.py          # Connection pool PostgreSQL
│   ├── models.py              # Modèles SQLAlchemy (table Deals)
│   ├── crud.py                # Opérations CRUD
│   └── init_schema.sql        # Schéma SQL initial
│
├── business_logic/
│   ├── __init__.py
│   ├── calculators.py         # Calcul probabilités & pondérations
│   ├── validators.py          # Validation données (CSV, formulaires)
│   └── filters.py             # Logique filtrage (secteur, statut, dates)
│
├── components/
│   ├── __init__.py
│   ├── kpi_cards.py           # Métriques flash (panier moyen, pipe total)
│   ├── sector_analysis.py     # Graphique barres par secteur
│   ├── funnel_chart.py        # Pipeline pondéré (entonnoir)
│   ├── deadline_table.py      # Liste deals avec échéances
│   └── csv_uploader.py        # Interface upload CSV
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py          # Formatage €, %, dates françaises
│   └── constants.py           # Constantes (statuts, probabilités)
│
└── tests/                      # Tests unitaires (future Phase 2)
    ├── __init__.py
    ├── test_calculators.py
    └── test_validators.py
```

---

## 🗄️ Schéma Base de Données

### Table `deals`

| Colonne | Type | Contraintes | Description |
|---------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Identifiant unique auto-incrémenté |
| `client` | VARCHAR(255) | NOT NULL | Nom du prospect/entreprise |
| `statut` | VARCHAR(50) | NOT NULL | Prospect, Qualifié, Négociation, Gagné |
| `montant_brut` | DECIMAL(12,2) | NOT NULL | Valeur totale du deal (€) |
| `probabilite` | DECIMAL(3,2) | NOT NULL | 0.10, 0.30, 0.70, 1.00 (auto-calculé) |
| `valeur_ponderee` | DECIMAL(12,2) | GENERATED | `montant_brut * probabilite` |
| `secteur` | VARCHAR(100) | | Secteur d'activité (ex: Tech, Sport) |
| `date_echeance` | DATE | | Date de clôture prévue |
| `assignee` | VARCHAR(100) | | Commercial responsable |
| `notes` | TEXT | | Détails additionnels |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Date de création |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Dernière modification |

### Index
```sql
CREATE INDEX idx_deals_statut ON deals(statut);
CREATE INDEX idx_deals_secteur ON deals(secteur);
CREATE INDEX idx_deals_date_echeance ON deals(date_echeance);
CREATE INDEX idx_deals_assignee ON deals(assignee);
```

### Règles Métier (Triggers)
```sql
-- Auto-update updated_at
CREATE TRIGGER update_deals_updated_at
  BEFORE UPDATE ON deals
  FOR EACH ROW
  EXECUTE FUNCTION update_timestamp();

-- Auto-calculate probabilite from statut
CREATE TRIGGER calculate_probabilite
  BEFORE INSERT OR UPDATE ON deals
  FOR EACH ROW
  EXECUTE FUNCTION set_probabilite_from_statut();
```

---

## 🔧 Configuration Environnement

### Variables d'Environnement (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@ep-cool-name.us-east-2.aws.neon.tech/crm_db?sslmode=require

# Application
APP_ENV=development  # development | production
DEBUG_MODE=true

# Streamlit Config
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
```

### Fichier requirements.txt

```txt
# Core
streamlit==1.32.0
python-dotenv==1.0.1

# Database
sqlalchemy==2.0.27
psycopg[binary]==3.1.18
alembic==1.13.1  # Migrations (Phase 2)

# Data Processing
pandas==2.2.1
numpy==1.26.4

# Visualisation
plotly==5.18.0

# Utils
python-dateutil==2.9.0
```

---

## 📊 Fonctionnalités MVP (Phase 1)

### 1. Import CSV
- Upload fichier `crm_prospects_demo.csv`
- Mapping colonnes automatique
- Validation données (montants > 0, dates valides)
- Calcul automatique probabilités selon statut
- Insertion batch en PostgreSQL

### 2. KPIs Flash
- **Pipeline pondéré total** : Somme `valeur_ponderee`
- **Panier moyen** : Moyenne `montant_brut`
- **Taux de conversion** : `(Deals gagnés / Total deals) * 100`
- **Nombre de deals** : Count par statut

### 3. Analyse par Secteur
- Graphique barres horizontales (Plotly)
- Montant total par secteur
- Top 5 secteurs à plus haut panier moyen
- Filtrable par statut

### 4. Gestion Échéances
- Liste des deals avec `date_echeance`
- **Alertes rouges** : Échéances dépassées (date < aujourd'hui)
- **À venir** : Prochains 30 jours
- Tri par date croissante

### 5. Navigation & Filtres
- Sidebar Streamlit :
  - Filtre par statut (multiselect)
  - Filtre par secteur (multiselect)
  - Filtre par commercial (multiselect)
  - Range de dates (date_input)
- Bouton "Reset filtres"

---

## 🚀 Roadmap d'Évolution

### Phase 1 : MVP (Actuel) - 3 jours
- ✅ Import CSV
- ✅ KPIs flash
- ✅ Analyse secteur
- ✅ Gestion échéances
- ✅ Filtres basiques

### Phase 2 : V1 (3-6 mois) - +1 semaine
- [ ] Saisie manuelle (formulaire CRUD)
- [ ] Authentification basique (streamlit-authenticator)
- [ ] Performance commerciale (analyse par assignee)
- [ ] Export Excel/PDF
- [ ] Filtres avancés (recherche textuelle)

### Phase 3 : V2 (6-12 mois) - +1 semaine
- [ ] Vitesse de vente (métriques temporelles)
- [ ] Simulateur "What-If" (impact +10% panier moyen)
- [ ] Relances automatiques (deals froids > 10j)
- [ ] Notifications email (échéances J-7)
- [ ] API REST (FastAPI endpoints)

### Phase 4 : Scale (12-18 mois) - Si nécessaire
- [ ] Migration React + FastAPI (si > 100 users)
- [ ] Permissions granulaires (RBAC)
- [ ] Mobile app (React Native)
- [ ] Intégrations tierces (Zapier, Stripe)

---

## 🔐 Sécurité

### Phase MVP (Usage Solo)
- ⚠️ **Pas d'authentification** : Accès local uniquement
- ✅ **Connection PostgreSQL SSL** : `sslmode=require`
- ✅ **Variables environnement** : Credentials hors Git
- ✅ **Validation inputs** : Protection SQL injection (SQLAlchemy)

### Phase Production (Future)
- [ ] Authentification multi-utilisateurs
- [ ] Row-Level Security (RLS) PostgreSQL
- [ ] HTTPS obligatoire
- [ ] Rate limiting
- [ ] Logs audit trail

---

## ⚡ Performance

### Optimisations Streamlit
```python
# Cache données database (refresh 5 min)
@st.cache_data(ttl=300)
def load_deals():
    return pd.read_sql_query("SELECT * FROM deals", engine)

# Cache calculs lourds
@st.cache_data
def calculate_sector_analysis(df):
    return df.groupby('secteur')['montant_brut'].sum()
```

### Optimisations PostgreSQL
- Index sur colonnes filtrées (`statut`, `secteur`, `date_echeance`)
- Connection pooling (SQLAlchemy `pool_size=5`)
- Query pagination (LIMIT/OFFSET pour grandes tables)

### Limites Connues
- Streamlit recharge script complet à chaque interaction
- Adapté pour < 50 utilisateurs simultanés
- Tables > 100k lignes : prévoir agrégations en DB

---

## 📦 Déploiement

### Local Development
```bash
# 1. Setup environnement
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Installer dépendances
pip install -r requirements.txt

# 3. Configurer .env
cp .env.example .env
# Éditer DATABASE_URL avec credentials Neon

# 4. Initialiser database
python -m database.init_schema

# 5. Lancer app
streamlit run app.py
```

### Production (Future Phase 2)
```bash
# 1. Build Docker image
docker build -t crm-dashboard .

# 2. Deploy Railway/Render
railway up  # ou render deploy

# 3. Variables environnement
railway variables set DATABASE_URL=postgresql://...
```

---

## 🧪 Tests & Qualité

### Phase MVP
- ⚠️ Pas de tests automatisés (priorisation vitesse)
- ✅ Tests manuels :
  - Import CSV avec données demo
  - Vérification calculs (probabilités, pondérations)
  - Test filtres et interactions

### Phase 2 (Future)

#### Tests Unitaires (Python)
```bash
# Tests unitaires
pytest tests/

# Coverage
pytest --cov=business_logic --cov-report=html
```

#### Tests End-to-End (Playwright)

**Installation** :
```bash
# Installer Playwright
pip install pytest-playwright
playwright install chromium

# Ou avec npm (si Node.js disponible)
npm install -D @playwright/test
npx playwright install
```

**Structure Tests E2E** :
```
tests/
├── e2e/
│   ├── __init__.py
│   ├── conftest.py              # Configuration pytest
│   ├── test_dashboard_flow.py   # Parcours utilisateur complet
│   ├── test_csv_upload.py       # Tests upload CSV
│   ├── test_filters.py          # Tests filtres sidebar
│   └── test_kpis.py             # Validation métriques
└── fixtures/
    └── test_data.csv            # Données de test
```

**Exemple Test** :
```python
# tests/e2e/test_dashboard_flow.py
import pytest
from playwright.sync_api import Page, expect

@pytest.fixture(scope="session")
def streamlit_url():
    return "http://localhost:8501"

def test_homepage_loads(page: Page, streamlit_url):
    """Vérifie que la page principale charge correctement"""
    page.goto(streamlit_url)
    expect(page).to_have_title("CRM Dashboard")

    # Vérifier présence KPIs
    expect(page.locator("text=Pipeline Pondéré")).to_be_visible()
    expect(page.locator("text=Panier Moyen")).to_be_visible()

def test_csv_upload_workflow(page: Page, streamlit_url):
    """Test complet d'upload CSV"""
    page.goto(streamlit_url)

    # Upload fichier
    page.locator("input[type='file']").set_input_files("tests/fixtures/test_data.csv")

    # Attendre traitement
    page.wait_for_selector("text=Import réussi", timeout=5000)

    # Vérifier données affichées
    expect(page.locator("text=10 deals importés")).to_be_visible()

def test_filters_interaction(page: Page, streamlit_url):
    """Test filtres sidebar"""
    page.goto(streamlit_url)

    # Ouvrir sidebar si fermée
    if not page.locator(".stSidebar").is_visible():
        page.locator("[data-testid='stSidebarCollapse']").click()

    # Sélectionner filtre statut
    page.locator("text=Statut").click()
    page.locator("text=Négociation").click()

    # Vérifier mise à jour tableau
    page.wait_for_timeout(1000)  # Attendre rerun Streamlit
    expect(page.locator(".stDataFrame")).to_contain_text("Négociation")

def test_kpi_calculations(page: Page, streamlit_url):
    """Validation calculs métriques"""
    page.goto(streamlit_url)

    # Récupérer valeur pipeline pondéré
    pipeline_value = page.locator("[data-testid='stMetricValue']").first.inner_text()

    # Vérifier format (doit contenir €)
    assert "€" in pipeline_value
    assert pipeline_value != "0 €"
```

**Configuration pytest** :
```python
# tests/e2e/conftest.py
import pytest
import subprocess
import time

@pytest.fixture(scope="session", autouse=True)
def start_streamlit():
    """Démarre Streamlit avant les tests"""
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Attendre démarrage
    time.sleep(5)

    yield

    # Arrêter à la fin
    process.terminate()
    process.wait()
```

**Exécution** :
```bash
# Tests E2E complets
pytest tests/e2e/

# Mode headed (voir navigateur)
pytest tests/e2e/ --headed

# Tests spécifiques
pytest tests/e2e/test_csv_upload.py -v

# Screenshots sur échec
pytest tests/e2e/ --screenshot on-failure
```

**Points d'Attention Streamlit** :
- Streamlit recharge la page à chaque interaction → utiliser `page.wait_for_timeout()` ou attendre sélecteurs
- Data-testids : Streamlit génère des IDs stables (`data-testid="stMetricValue"`)
- Sidebar : Peut être cachée sur mobile → vérifier visibilité
- File uploader : Utiliser `set_input_files()` pour upload programmatique

---

## 📚 Documentation Additionnelle

### Références Techniques
- [Streamlit Docs](https://docs.streamlit.io/)
- [SQLAlchemy 2.0 Guide](https://docs.sqlalchemy.org/en/20/)
- [Neon PostgreSQL](https://neon.tech/docs)
- [Plotly Python](https://plotly.com/python/)

### Fichiers Liés
- `PRD.md` : Spécifications fonctionnelles complètes
- `README.md` : Instructions setup et usage
- `.env.example` : Template configuration

---

## 🤝 Décisions Architecturales Clés

### 1. Pourquoi Streamlit plutôt que React ?
- **Temps dev** : 3 jours vs 15-20 jours
- **Complexité** : Python monolithe vs frontend/backend séparés
- **Usage** : < 50 users parfaitement adapté
- **Migration** : Possible vers React si > 100 users dans 12-18 mois

### 2. Pourquoi PostgreSQL plutôt que SQLite ?
- **Multi-users** : Évolution prévue 6-12 mois
- **Volume** : Support tera-octets vs 1 GB SQLite
- **Intégrations** : LISTEN/NOTIFY pour webhooks futures
- **Migration évitée** : +1 jour dev maintenant = -5 jours migration future

### 3. Pourquoi Neon plutôt que Supabase/Railway ?
- **Simplicité** : Setup 5 minutes, zéro configuration
- **Générosité** : 10 GB gratuit (vs 500 MB Supabase)
- **Focus** : Pure PostgreSQL, pas de services annexes
- **Serverless** : Scaling automatique inclus

### 4. Pourquoi pas d'authentification au MVP ?
- **Scope** : Usage solo fondateur Phase 1
- **Vitesse** : Économise 1-2 jours dev
- **Flexibilité** : Ajout Phase 2 avec streamlit-authenticator (simple)
- **Sécurité** : Accès local = pas d'exposition internet

---

## ✅ Checklist de Démarrage

- [ ] Créer compte Neon.tech
- [ ] Provisionner database PostgreSQL
- [ ] Cloner/créer structure projet
- [ ] Configurer .env avec DATABASE_URL
- [ ] Installer dépendances Python
- [ ] Initialiser schéma database
- [ ] Tester connection PostgreSQL
- [ ] Importer CSV demo
- [ ] Valider calculs automatiques
- [ ] Lancer Streamlit localement

**Temps estimé** : 3 jours (MVP complet)

---

**Contact** : Pour questions/clarifications sur architecture
**Dernière mise à jour** : 2025-02-05
