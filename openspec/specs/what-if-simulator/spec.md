### Requirement: Simulateur What-If variation panier moyen
Le système SHALL fournir un simulateur interactif permettant de projeter l'impact d'une variation du panier moyen sur le pipeline pondéré total.

#### Scenario: Calcul projection avec variation positive
- **WHEN** l'utilisateur sélectionne une variation de +10% du panier moyen
- **THEN** le système affiche le nouveau pipeline pondéré projeté calculé comme : pipeline_actuel * (1 + variation/100)

#### Scenario: Calcul projection avec variation négative
- **WHEN** l'utilisateur sélectionne une variation de -10% du panier moyen
- **THEN** le système affiche le nouveau pipeline pondéré projeté calculé comme : pipeline_actuel * (1 + variation/100)

#### Scenario: Variation à zéro
- **WHEN** l'utilisateur positionne le curseur à 0%
- **THEN** le pipeline projeté affiché est égal au pipeline actuel

### Requirement: Interface curseur interactif
Le système SHALL afficher un curseur (range slider) HTML permettant de choisir une variation du panier moyen entre -50% et +50% par incréments de 5%.

#### Scenario: Curseur avec valeur par défaut
- **WHEN** le dashboard charge la section simulateur
- **THEN** le curseur est positionné à 0% avec le pipeline actuel affiché

#### Scenario: Mise à jour temps réel
- **WHEN** l'utilisateur déplace le curseur
- **THEN** les valeurs projetées (nouveau panier moyen, nouveau pipeline pondéré, différence en €) se mettent à jour instantanément sans appel réseau

#### Scenario: Affichage de la différence
- **WHEN** l'utilisateur sélectionne une variation non nulle
- **THEN** le système affiche la différence absolue en € et en pourcentage entre le pipeline actuel et le pipeline projeté, avec un indicateur visuel vert (hausse) ou rouge (baisse)

### Requirement: Calcul côté client JavaScript
Le système SHALL effectuer tous les calculs du simulateur What-If côté client en JavaScript, à partir des données KPIs déjà chargées.

#### Scenario: Données source depuis les KPIs
- **WHEN** le simulateur initialise ses calculs
- **THEN** il utilise les valeurs pipeline_pondere et panier_moyen déjà récupérées par l'appel GET /api/kpis

#### Scenario: Pas d'appel réseau supplémentaire
- **WHEN** l'utilisateur interagit avec le curseur
- **THEN** aucune requête HTTP n'est envoyée au serveur

### Requirement: Affichage section Simulateur dans le dashboard
Le système SHALL afficher une section dédiée "Simulateur What-If" dans le dashboard, positionnée après la section vitesse de vente.

#### Scenario: Composition de la section
- **WHEN** le dashboard charge la section simulateur
- **THEN** il affiche le curseur, le pourcentage de variation sélectionné, le nouveau panier moyen projeté, le nouveau pipeline projeté et la différence avec l'actuel

#### Scenario: Responsive mobile
- **WHEN** le dashboard est affiché sur un écran mobile (< 768px)
- **THEN** la section simulateur s'adapte en pleine largeur avec les éléments empilés verticalement
