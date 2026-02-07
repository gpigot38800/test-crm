## ADDED Requirements

### Requirement: Exposition gestion échéances via API REST
Le système SHALL exposer la gestion des échéances via endpoint GET /api/analytics/deadlines retournant JSON pour tableaux HTML au lieu de dataframes Streamlit.

#### Scenario: Endpoint analytics échéances
- **WHEN** un client envoie GET /api/analytics/deadlines
- **THEN** le système retourne JSON avec overdue_deals, upcoming_deals et statistics

#### Scenario: Calcul échéances dépassées
- **WHEN** l'API calcule les retards
- **THEN** le système filtre les deals avec date_echeance < aujourd'hui

#### Scenario: Calcul jours de retard
- **WHEN** un deal en retard est traité
- **THEN** le système calcule (aujourd'hui - date_echeance).days pour chaque deal

#### Scenario: Calcul échéances à venir 30 jours
- **WHEN** l'API calcule les échéances futures
- **THEN** le système filtre les deals avec aujourd'hui <= date_echeance <= aujourd'hui + 30 jours

#### Scenario: Calcul jours restants
- **WHEN** un deal à venir est traité
- **THEN** le système calcule (date_echeance - aujourd'hui).days pour chaque deal

#### Scenario: Statistiques échéances
- **WHEN** l'API génère les statistiques
- **THEN** le système retourne nb_overdue, nb_upcoming, montant_upcoming et pct_with_deadline

#### Scenario: Tri par urgence
- **WHEN** les deals en retard sont retournés
- **THEN** le système trie par date_echeance croissante (les plus anciens en premier)

#### Scenario: Deal le plus urgent
- **WHEN** des deals en retard existent
- **THEN** le système identifie et retourne le deal avec le plus grand nombre de jours de retard
