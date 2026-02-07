## ADDED Requirements

### Requirement: Performance analytics API endpoint
Le système SHALL exposer un endpoint GET /api/analytics/performance retournant les métriques de performance par commercial (assignee).

#### Scenario: Récupération des performances avec données
- **WHEN** un client envoie GET /api/analytics/performance et des deals avec assignees existent
- **THEN** le système retourne un JSON avec pour chaque assignee : nombre de deals, montant total, pipeline pondéré, deals gagnés, taux de conversion, et panier moyen

#### Scenario: Récupération des performances sans données
- **WHEN** un client envoie GET /api/analytics/performance et aucun deal n'existe
- **THEN** le système retourne un JSON avec une liste vide et des statistiques à zéro

#### Scenario: Deals sans assignee
- **WHEN** des deals existent sans valeur assignee
- **THEN** le système les regroupe sous le libellé "Non assigné" dans les métriques

#### Scenario: Support des filtres sur les performances
- **WHEN** un client envoie GET /api/analytics/performance avec des query parameters de filtrage (statut, secteur, date_from, date_to)
- **THEN** le système retourne les métriques calculées uniquement sur les deals correspondant aux filtres

### Requirement: Performance chart visualization
Le système SHALL afficher un graphique Chart.js barres verticales groupées montrant le nombre de deals et le taux de conversion par commercial.

#### Scenario: Affichage du graphique performance
- **WHEN** le dashboard charge la section performance et des deals avec assignees existent
- **THEN** le système affiche un graphique barres groupées avec une barre bleue (nb deals) et une barre verte (taux de conversion %) par assignee

#### Scenario: Graphique vide
- **WHEN** aucun deal n'existe en base
- **THEN** le système affiche un message "Aucune donnée de performance disponible" à la place du graphique

#### Scenario: Tooltips du graphique
- **WHEN** l'utilisateur survole une barre du graphique
- **THEN** le système affiche un tooltip avec la valeur exacte (nombre de deals ou pourcentage de conversion)

### Requirement: Performance summary table
Le système SHALL afficher un tableau récapitulatif des performances par commercial sous le graphique.

#### Scenario: Affichage du tableau performance
- **WHEN** le dashboard charge la section performance et des données existent
- **THEN** le système affiche un tableau avec colonnes : Commercial, Nb Deals, Montant Total, Pipeline Pondéré, Panier Moyen, Taux Conversion

#### Scenario: Tri par pipeline pondéré
- **WHEN** le tableau de performance est affiché
- **THEN** le système trie les commerciaux par pipeline pondéré décroissant (meilleur performeur en premier)

#### Scenario: Formatage des valeurs
- **WHEN** le tableau de performance est affiché
- **THEN** le système formate les montants en euros (XX XXX €), les taux en pourcentage (XX.X%), et les nombres entiers sans décimales

### Requirement: Performance section layout
Le système SHALL positionner la section performance commerciale entre l'analyse par secteur et la gestion des échéances dans le dashboard.

#### Scenario: Position dans le dashboard
- **WHEN** le dashboard est affiché avec toutes les sections
- **THEN** la section "Performance Commerciale" apparaît après "Analyse par Secteur" et avant "Gestion des Échéances"

#### Scenario: Responsive layout
- **WHEN** la section performance est affichée sur mobile (< 640px)
- **THEN** le graphique et le tableau s'empilent verticalement et occupent 100% de la largeur
