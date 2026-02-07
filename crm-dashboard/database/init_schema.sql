-- Schema version: 2.0 - Migration PostgreSQL
-- Dashboard CRM - Table deals

CREATE TABLE IF NOT EXISTS deals (
    id SERIAL PRIMARY KEY,
    client VARCHAR(255) NOT NULL,
    statut VARCHAR(50) NOT NULL,
    montant_brut NUMERIC(12,2) NOT NULL,
    probabilite NUMERIC(3,2) NOT NULL,
    valeur_ponderee NUMERIC(12,2) NOT NULL,
    secteur VARCHAR(100),
    date_echeance DATE,
    assignee VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index pour les filtres fréquents
CREATE INDEX IF NOT EXISTS idx_deals_statut ON deals(statut);
CREATE INDEX IF NOT EXISTS idx_deals_secteur ON deals(secteur);
CREATE INDEX IF NOT EXISTS idx_deals_date_echeance ON deals(date_echeance);
CREATE INDEX IF NOT EXISTS idx_deals_assignee ON deals(assignee);

-- Tables connecteurs API
CREATE TABLE IF NOT EXISTS connector_configs (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) UNIQUE NOT NULL,
    api_token TEXT,
    base_id VARCHAR(255),
    table_name VARCHAR(255),
    field_mapping TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sync_logs (
    id SERIAL PRIMARY KEY,
    provider VARCHAR(50) NOT NULL,
    direction VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    records_processed INTEGER DEFAULT 0,
    records_created INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);
