## ADDED Requirements

### Requirement: Graphique Chart.js pour montants totaux par secteur
Le système SHALL afficher un graphique en barres horizontales Chart.js montrant le montant total par secteur avec labels lisibles.

#### Scenario: Affichage graphique secteurs
- **WHEN** le dashboard charge avec des deals ayant des secteurs
- **THEN** le système affiche un graphique Chart.js avec barres horizontales, un axe par secteur et montants en euros

#### Scenario: Labels secteurs lisibles
- **WHEN** le graphique secteurs est affiché
- **THEN** le système affiche tous les noms de secteurs complets et lisibles sans troncature

#### Scenario: Tooltips personnalisés
- **WHEN** l'utilisateur survole une barre du graphique
- **THEN** le système affiche un tooltip avec nom du secteur et montant formaté en euros

#### Scenario: Couleurs cohérentes
- **WHEN** le graphique secteurs est affiché
- **THEN** le système utilise une palette de bleus pour les barres

### Requirement: Graphique Chart.js pour top 5 paniers moyens
Le système SHALL afficher un graphique en barres horizontales Chart.js montrant les 5 secteurs avec le meilleur panier moyen.

#### Scenario: Affichage top 5 secteurs
- **WHEN** le dashboard charge avec au moins 5 secteurs
- **THEN** le système affiche un graphique Chart.js avec les 5 secteurs ayant le panier moyen le plus élevé

#### Scenario: Palette de couleurs verts
- **WHEN** le graphique top 5 est affiché
- **THEN** le système utilise une palette de verts pour les barres

#### Scenario: Tri décroissant visuel
- **WHEN** le graphique top 5 est affiché
- **THEN** le système affiche les secteurs du meilleur panier moyen en bas au moins bon en haut

### Requirement: Tableau récapitulatif secteurs HTML
Le système SHALL afficher un tableau HTML avec montant total, panier moyen, nombre de deals et valeur pondérée par secteur.

#### Scenario: Colonnes du tableau
- **WHEN** le tableau secteurs est affiché
- **THEN** le système affiche 5 colonnes : Secteur, Montant Total, Panier Moyen, Nombre Deals, Valeur Pondérée

#### Scenario: Formatage montants
- **WHEN** le tableau secteurs est affiché
- **THEN** le système formate tous les montants avec séparateurs milliers et symbole €

#### Scenario: Tri par montant total
- **WHEN** le tableau secteurs est affiché
- **THEN** le système trie les secteurs par montant total décroissant

### Requirement: Tableaux HTML échéances
Le système SHALL afficher deux tableaux HTML pour échéances dépassées et échéances à venir dans les 30 jours.

#### Scenario: Tableau échéances dépassées
- **WHEN** des deals ont une date d'échéance < aujourd'hui
- **THEN** le système affiche un tableau avec client, statut, montant, date échéance, jours de retard, secteur et commercial

#### Scenario: Tableau échéances à venir
- **WHEN** des deals ont une date d'échéance entre aujourd'hui et +30 jours
- **THEN** le système affiche un tableau avec client, statut, montant, date échéance, jours restants, secteur et commercial

#### Scenario: Indicateur visuel retard
- **WHEN** le tableau échéances dépassées est affiché avec au moins 1 deal
- **THEN** le système affiche une alerte rouge avec le nombre de deals en retard

#### Scenario: Calcul jours de retard
- **WHEN** un deal en retard est affiché
- **THEN** le système calcule et affiche le nombre de jours entre la date d'échéance et aujourd'hui

### Requirement: Animations et transitions fluides
Le système SHALL appliquer des animations CSS fluides pour améliorer l'expérience utilisateur.

#### Scenario: Animation apparition graphiques
- **WHEN** les graphiques Chart.js sont chargés
- **THEN** le système anime l'apparition des barres avec une transition de 800ms

#### Scenario: Hover effects
- **WHEN** l'utilisateur survole une card KPI
- **THEN** le système applique une légère élévation (shadow) avec transition de 200ms
