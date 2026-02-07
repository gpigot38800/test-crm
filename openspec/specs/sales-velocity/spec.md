### Requirement: Calcul de la vitesse de vente
Le système SHALL calculer la durée moyenne de conversion des deals en jours, définie comme la différence entre `updated_at` et `created_at` pour les deals au statut "Gagné".

#### Scenario: Calcul vitesse moyenne globale
- **WHEN** le système calcule la vitesse de vente
- **THEN** il retourne la moyenne en jours de `updated_at - created_at` pour tous les deals dont le statut est "Gagné"

#### Scenario: Aucun deal gagné
- **WHEN** aucun deal n'a le statut "Gagné"
- **THEN** le système retourne 0 comme vitesse de vente moyenne

### Requirement: Ventilation de la vitesse par groupe
Le système SHALL ventiler la vitesse de vente par secteur et par commercial (assignee), permettant d'identifier les segments les plus rapides à convertir.

#### Scenario: Vitesse par secteur
- **WHEN** le système calcule la vitesse de vente ventilée par secteur
- **THEN** il retourne pour chaque secteur la durée moyenne en jours des deals "Gagné" de ce secteur

#### Scenario: Vitesse par commercial
- **WHEN** le système calcule la vitesse de vente ventilée par commercial
- **THEN** il retourne pour chaque assignee la durée moyenne en jours des deals "Gagné" gérés par ce commercial

#### Scenario: Secteur ou commercial sans deal gagné
- **WHEN** un secteur ou commercial n'a aucun deal "Gagné"
- **THEN** il est exclu des résultats de ventilation

### Requirement: Endpoint API vitesse de vente
Le système SHALL exposer un endpoint GET /api/analytics/velocity retournant les métriques de vitesse de vente au format JSON.

#### Scenario: Réponse endpoint velocity
- **WHEN** un client envoie GET /api/analytics/velocity
- **THEN** le système retourne JSON avec vitesse_moyenne_jours, ventilation par secteur (velocity_by_sector) et par commercial (velocity_by_assignee)

#### Scenario: Support des filtres existants
- **WHEN** un client envoie GET /api/analytics/velocity avec des paramètres de filtre (statut, secteur, assignee, dates)
- **THEN** le calcul de vitesse s'applique uniquement aux deals correspondant aux filtres

### Requirement: Affichage section Vitesse de Vente dans le dashboard
Le système SHALL afficher une section dédiée "Vitesse de Vente" dans le dashboard avec un KPI principal et un graphique à barres.

#### Scenario: KPI vitesse moyenne
- **WHEN** le dashboard charge la section vitesse de vente
- **THEN** il affiche la vitesse moyenne globale en jours avec un libellé "Vitesse de Vente Moyenne"

#### Scenario: Graphique barres par secteur
- **WHEN** le dashboard affiche la section vitesse de vente
- **THEN** il affiche un graphique à barres horizontales Chart.js montrant la durée moyenne par secteur, triée par durée décroissante

#### Scenario: Responsive mobile
- **WHEN** le dashboard est affiché sur un écran mobile (< 768px)
- **THEN** la section vitesse de vente s'adapte en pleine largeur avec le graphique empilé sous le KPI
