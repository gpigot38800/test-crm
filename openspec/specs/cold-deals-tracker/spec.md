### Requirement: Détection des deals froids
Le système SHALL identifier les deals "froids" définis comme les deals dont le champ `updated_at` date de plus de 10 jours et dont le statut n'est pas "Gagné".

#### Scenario: Deal froid détecté
- **WHEN** un deal a un `updated_at` antérieur de plus de 10 jours par rapport à la date actuelle et son statut n'est pas "Gagné"
- **THEN** le système le classe comme deal froid

#### Scenario: Deal gagné exclu
- **WHEN** un deal a un `updated_at` antérieur de plus de 10 jours mais son statut est "Gagné"
- **THEN** le système ne le classe pas comme deal froid

#### Scenario: Deal récemment mis à jour exclu
- **WHEN** un deal a un `updated_at` de moins de 10 jours
- **THEN** le système ne le classe pas comme deal froid, quel que soit son statut

### Requirement: Endpoint API deals froids
Le système SHALL exposer un endpoint GET /api/analytics/cold-deals retournant la liste des deals froids au format JSON.

#### Scenario: Réponse endpoint cold-deals
- **WHEN** un client envoie GET /api/analytics/cold-deals
- **THEN** le système retourne JSON avec la liste des deals froids incluant pour chaque deal : id, client, statut, montant_brut, secteur, assignee, date_echeance, jours_inactifs (nombre de jours depuis updated_at)

#### Scenario: Statistiques agrégées
- **WHEN** un client envoie GET /api/analytics/cold-deals
- **THEN** la réponse inclut des stats agrégées : nb_cold_deals (nombre total), montant_total_cold (somme des montants bruts des deals froids)

#### Scenario: Support des filtres existants
- **WHEN** un client envoie GET /api/analytics/cold-deals avec des paramètres de filtre (statut, secteur, assignee)
- **THEN** la détection de deals froids s'applique uniquement aux deals correspondant aux filtres

#### Scenario: Aucun deal froid
- **WHEN** tous les deals ont été mis à jour dans les 10 derniers jours ou sont au statut "Gagné"
- **THEN** le système retourne une liste vide et nb_cold_deals à 0

### Requirement: Marquage visuel des deals froids dans le dashboard
Le système SHALL afficher un marquage visuel distinct pour les deals froids dans le dashboard, avec un badge compteur et une liste dédiée.

#### Scenario: Badge compteur deals froids dans les KPIs
- **WHEN** le dashboard charge et qu'il existe des deals froids
- **THEN** un badge avec le nombre de deals froids est affiché dans la section KPIs avec une couleur d'alerte (rouge si > 5 deals, orange sinon)

#### Scenario: Liste dédiée des deals froids
- **WHEN** le dashboard charge la section deals froids
- **THEN** il affiche un tableau listant chaque deal froid avec client, statut, montant, secteur, commercial et nombre de jours d'inactivité, trié par jours_inactifs décroissant

#### Scenario: Indicateur visuel par ancienneté
- **WHEN** un deal froid est affiché dans la liste
- **THEN** il affiche un badge orange si inactif 10-20 jours, rouge si inactif > 20 jours

#### Scenario: Aucun deal froid
- **WHEN** aucun deal froid n'est détecté
- **THEN** la section affiche un message "Aucun deal froid — tous les deals sont actifs" et le badge compteur n'apparaît pas

#### Scenario: Responsive mobile
- **WHEN** le dashboard est affiché sur un écran mobile (< 768px)
- **THEN** la section deals froids s'adapte en pleine largeur avec un tableau scrollable horizontalement

### Requirement: Seuil de détection configurable
Le système SHALL définir le seuil de détection des deals froids (10 jours par défaut) comme constante dans utils/constants.py.

#### Scenario: Constante COLD_DEAL_THRESHOLD_DAYS
- **WHEN** le système évalue si un deal est froid
- **THEN** il utilise la valeur de COLD_DEAL_THRESHOLD_DAYS définie dans utils/constants.py (par défaut 10)
