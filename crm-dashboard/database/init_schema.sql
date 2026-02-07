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
