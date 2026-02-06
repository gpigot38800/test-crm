-- Schema version: 1.0 - Initial MVP
-- Dashboard CRM - Table deals

CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client TEXT NOT NULL,
    statut TEXT NOT NULL,
    montant_brut REAL NOT NULL,
    probabilite REAL NOT NULL,
    valeur_ponderee REAL NOT NULL,
    secteur TEXT,
    date_echeance DATE,
    assignee TEXT,
    notes TEXT
);
