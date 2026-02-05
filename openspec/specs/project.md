# CRM Dashboard - Project Specification

## Project Overview

**Name**: CRM Dashboard
**Type**: Data Dashboard Application
**Target User**: Company Founder (personal use)
**Primary Goal**: Maximize deal volume and deal value
**Philosophy**: No technical frills, only decision-making indicators
**Current Phase**: MVP Phase 1
**Location**: `C:\Users\geoff\OneDrive\Documents\CLAUDE PROJET\CRM TEST\crm-dashboard`

## Vision

Dashboard CRM for founder with objective to maximize volume and value of deals, designed to evolve towards multi-user usage in 6-12 months.

### Guiding Principles
- ✅ **Development Speed**: MVP in 3 days
- ✅ **Architectural Simplicity**: Monolithic Python stack
- ✅ **Prepared Scalability**: PostgreSQL from the start
- ✅ **Controlled Costs**: Free tiers for launch

## Tech Stack

### Frontend & Backend
- **Framework**: Streamlit 1.32+
- **Language**: Python 3.11+
- **Architecture**: Monolith (frontend + backend in app.py)

**Justification**:
- Rapid development (pure Python, no JS/HTML/CSS)
- Excellent data science integration (Pandas, NumPy native)
- Suitable for 1-50 users
- Future migration to React possible if needed (> 100 users)

### Database
- **DBMS**: PostgreSQL 15+
- **Hosting**: Neon.tech (free tier)
  - Limit: 10 GB storage
  - Serverless with automatic scaling
  - Connection string: `postgresql://user:pass@host/dbname`
- **ORM**: SQLAlchemy 2.0+
- **Driver**: psycopg3

**Justification**:
- Multi-user ready (vs SQLite limited to 1 write)
- Unlimited scalability (terabytes supported)
- Avoids database migration in 6 months
- Native granular permissions (GRANT/REVOKE)
- Universal standard (guaranteed portability)

### Data Processing & Visualization
- **Data manipulation**: Pandas 2.2+, NumPy 1.26+
- **Charts**: Plotly 5.18+ (interactivity)
- **CSV parsing**: Pandas `read_csv()` (native)
- **Business calculations**: Pure Python (probabilities, weightings)

### Deployment
- **MVP Phase**: Local only
  - Launch: `streamlit run app.py`
  - Access: `http://localhost:8501`
  - No container to simplify dev
- **Production Phase (future)**:
  - Docker + Railway/Render
  - Environment variables (.env)
  - CI/CD GitHub Actions

## Project Structure

```
crm-dashboard/
├── app.py                      # Streamlit entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Exclude .env, __pycache__, etc.
│
├── database/
│   ├── __init__.py
│   ├── connection.py          # PostgreSQL connection pool
│   ├── models.py              # SQLAlchemy models (Deals table)
│   ├── crud.py                # CRUD operations
│   └── init_schema.sql        # Initial SQL schema
│
├── business_logic/
│   ├── __init__.py
│   ├── calculators.py         # Probability & weighting calculations
│   ├── validators.py          # Data validation (CSV, forms)
│   └── filters.py             # Filtering logic (sector, status, dates)
│
├── components/
│   ├── __init__.py
│   ├── kpi_cards.py           # Flash metrics (avg basket, total pipe)
│   ├── sector_analysis.py     # Bar chart by sector
│   ├── funnel_chart.py        # Weighted pipeline (funnel)
│   ├── deadline_table.py      # Deals list with deadlines
│   └── csv_uploader.py        # CSV upload interface
│
├── utils/
│   ├── __init__.py
│   ├── formatters.py          # Formatting €, %, French dates
│   └── constants.py           # Constants (statuses, probabilities)
│
└── tests/                      # Unit tests (future Phase 2)
    ├── __init__.py
    ├── test_calculators.py
    └── test_validators.py
```

## Database Schema

### Table `deals`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-incremented unique identifier |
| `client` | VARCHAR(255) | NOT NULL | Prospect/company name |
| `statut` | VARCHAR(50) | NOT NULL | Prospect, Qualifié, Négociation, Gagné |
| `montant_brut` | DECIMAL(12,2) | NOT NULL | Total deal value (€) |
| `probabilite` | DECIMAL(3,2) | NOT NULL | 0.10, 0.30, 0.70, 1.00 (auto-calculated) |
| `valeur_ponderee` | DECIMAL(12,2) | GENERATED | `montant_brut * probabilite` |
| `secteur` | VARCHAR(100) | | Activity sector (e.g., Tech, Sport) |
| `date_echeance` | DATE | | Expected closing date |
| `assignee` | VARCHAR(100) | | Responsible salesperson |
| `notes` | TEXT | | Additional details |
| `created_at` | TIMESTAMP | DEFAULT NOW() | Creation date |
| `updated_at` | TIMESTAMP | DEFAULT NOW() | Last modification |

### Indexes
```sql
CREATE INDEX idx_deals_statut ON deals(statut);
CREATE INDEX idx_deals_secteur ON deals(secteur);
CREATE INDEX idx_deals_date_echeance ON deals(date_echeance);
CREATE INDEX idx_deals_assignee ON deals(assignee);
```

### Business Rules (Triggers)
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

## Business Logic

### Status & Probability Mapping
- **Prospect**: 10% probability
- **Qualifié**: 30% probability
- **Négociation**: 70% probability
- **Gagné**: 100% probability

### Calculated Fields
- **Valeur Pondérée**: `montant_brut * probabilite`
- **Panier Moyen**: Average of `montant_brut`
- **Taux de Conversion**: `(Won deals / Total deals) * 100`

## Development Conventions

### Python Code Style
- Follow PEP 8
- Type hints for function signatures
- Docstrings for modules and functions
- Use SQLAlchemy ORM (no raw SQL in business logic)

### Streamlit Patterns
```python
# Cache database data (5 min refresh)
@st.cache_data(ttl=300)
def load_deals():
    return pd.read_sql_query("SELECT * FROM deals", engine)

# Cache heavy calculations
@st.cache_data
def calculate_sector_analysis(df):
    return df.groupby('secteur')['montant_brut'].sum()
```

### Database Optimizations
- Index on filtered columns (`statut`, `secteur`, `date_echeance`)
- Connection pooling (SQLAlchemy `pool_size=5`)
- Query pagination (LIMIT/OFFSET for large tables)

### File Naming
- Snake_case for Python files and functions
- PascalCase for classes
- UPPER_CASE for constants

## Environment Variables

Required in `.env`:
```bash
# Database
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Application
APP_ENV=development  # development | production
DEBUG_MODE=true

# Streamlit Config
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
```

## Dependencies (requirements.txt)

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

# Visualization
plotly==5.18.0

# Utils
python-dateutil==2.9.0
```

## MVP Features (Phase 1)

### 1. CSV Import
- Upload `crm_prospects_demo.csv` file
- Automatic column mapping
- Data validation (amounts > 0, valid dates)
- Automatic probability calculation by status
- Batch insertion in PostgreSQL

### 2. Flash KPIs
- **Weighted Pipeline Total**: Sum of `valeur_ponderee`
- **Average Basket**: Average of `montant_brut`
- **Conversion Rate**: `(Won deals / Total deals) * 100`
- **Deal Count**: Count by status

### 3. Sector Analysis
- Horizontal bar chart (Plotly)
- Total amount by sector
- Top 5 sectors by highest average basket
- Filterable by status

### 4. Deadline Management
- List of deals with `date_echeance`
- **Red alerts**: Overdue deadlines (date < today)
- **Upcoming**: Next 30 days
- Sort by ascending date

### 5. Navigation & Filters
- Streamlit sidebar:
  - Filter by status (multiselect)
  - Filter by sector (multiselect)
  - Filter by salesperson (multiselect)
  - Date range (date_input)
- "Reset filters" button

## Development Workflow

### Local Setup
```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env
cp .env.example .env
# Edit DATABASE_URL with Neon credentials

# 4. Initialize database
python -m database.init_schema

# 5. Launch app
streamlit run app.py
```

### Testing (Phase 2)
```bash
# Unit tests
pytest tests/

# Coverage
pytest --cov=business_logic --cov-report=html

# E2E tests (Playwright)
pytest tests/e2e/ --headed
```

## Roadmap

### Phase 1: MVP (Current) - 3 days
- ✅ CSV import
- ✅ Flash KPIs
- ✅ Sector analysis
- ✅ Deadline management
- ✅ Basic filters

### Phase 2: V1 (3-6 months) - +1 week
- [ ] Manual entry (CRUD form)
- [ ] Basic authentication (streamlit-authenticator)
- [ ] Sales performance (analysis by assignee)
- [ ] Excel/PDF export
- [ ] Advanced filters (text search)

### Phase 3: V2 (6-12 months) - +1 week
- [ ] Sales velocity (time metrics)
- [ ] "What-If" simulator (impact of +10% basket)
- [ ] Automatic reminders (cold deals > 10 days)
- [ ] Email notifications (deadlines D-7)
- [ ] REST API (FastAPI endpoints)

### Phase 4: Scale (12-18 months) - If needed
- [ ] React + FastAPI migration (if > 100 users)
- [ ] Granular permissions (RBAC)
- [ ] Mobile app (React Native)
- [ ] Third-party integrations (Zapier, Stripe)

## Security Considerations

### MVP Phase (Solo Use)
- ⚠️ **No authentication**: Local access only
- ✅ **PostgreSQL SSL connection**: `sslmode=require`
- ✅ **Environment variables**: Credentials outside Git
- ✅ **Input validation**: SQL injection protection (SQLAlchemy)

### Production Phase (Future)
- [ ] Multi-user authentication
- [ ] Row-Level Security (RLS) PostgreSQL
- [ ] Mandatory HTTPS
- [ ] Rate limiting
- [ ] Audit trail logs

## Known Limitations

- Streamlit reloads full script on each interaction
- Suitable for < 50 simultaneous users
- Tables > 100k rows: plan for DB aggregations

## Key Architectural Decisions

### Why Streamlit vs React?
- **Dev time**: 3 days vs 15-20 days
- **Complexity**: Python monolith vs separate frontend/backend
- **Usage**: < 50 users perfectly suited
- **Migration**: Possible to React if > 100 users in 12-18 months

### Why PostgreSQL vs SQLite?
- **Multi-users**: Evolution planned 6-12 months
- **Volume**: Terabyte support vs 1 GB SQLite
- **Integrations**: LISTEN/NOTIFY for future webhooks
- **Migration avoided**: +1 day dev now = -5 days future migration

### Why Neon vs Supabase/Railway?
- **Simplicity**: 5-minute setup, zero configuration
- **Generosity**: 10 GB free (vs 500 MB Supabase)
- **Focus**: Pure PostgreSQL, no ancillary services
- **Serverless**: Automatic scaling included

## References

- PRD: `PRD.md`
- Architecture: `ARCHITECTURE.md`
- [Streamlit Docs](https://docs.streamlit.io/)
- [SQLAlchemy 2.0 Guide](https://docs.sqlalchemy.org/en/20/)
- [Neon PostgreSQL](https://neon.tech/docs)
- [Plotly Python](https://plotly.com/python/)
