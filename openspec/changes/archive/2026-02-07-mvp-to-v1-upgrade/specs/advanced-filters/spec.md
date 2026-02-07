## ADDED Requirements

### Requirement: Filter sidebar layout
Le système SHALL afficher une sidebar de filtres à gauche du dashboard, collapsible sur mobile.

#### Scenario: Affichage sidebar sur desktop
- **WHEN** l'interface est affichée sur un écran >= 1024px
- **THEN** le système affiche une sidebar fixe de 250px à gauche avec les filtres, et le contenu principal occupe l'espace restant

#### Scenario: Sidebar collapsible sur mobile
- **WHEN** l'interface est affichée sur un écran < 1024px
- **THEN** la sidebar est masquée par défaut et un bouton hamburger dans le header permet de l'afficher en overlay

#### Scenario: Fermeture sidebar mobile
- **WHEN** l'utilisateur clique en dehors de la sidebar ouverte sur mobile
- **THEN** le système referme la sidebar

### Requirement: Status multi-select filter
Le système SHALL permettre de filtrer les deals par un ou plusieurs statuts via des checkboxes.

#### Scenario: Filtrage par statut unique
- **WHEN** l'utilisateur coche uniquement "Négociation" dans le filtre statut
- **THEN** le système recharge toutes les sections du dashboard (KPIs, graphiques, tableaux) en affichant uniquement les deals en Négociation

#### Scenario: Filtrage par statuts multiples
- **WHEN** l'utilisateur coche "Prospect" et "Qualifié" dans le filtre statut
- **THEN** le système affiche uniquement les deals ayant le statut Prospect ou Qualifié

#### Scenario: Aucun statut sélectionné
- **WHEN** l'utilisateur décoche tous les statuts
- **THEN** le système affiche tous les deals (équivalent à aucun filtre statut)

### Requirement: Sector multi-select filter
Le système SHALL permettre de filtrer les deals par un ou plusieurs secteurs via des checkboxes.

#### Scenario: Filtrage par secteur
- **WHEN** l'utilisateur coche "Tech" dans le filtre secteur
- **THEN** le système recharge le dashboard en affichant uniquement les deals du secteur Tech

#### Scenario: Liste dynamique des secteurs
- **WHEN** la sidebar est affichée
- **THEN** le système liste uniquement les secteurs présents dans la base de données (pas de valeurs en dur)

### Requirement: Assignee multi-select filter
Le système SHALL permettre de filtrer les deals par un ou plusieurs commerciaux via des checkboxes.

#### Scenario: Filtrage par commercial
- **WHEN** l'utilisateur coche un commercial dans le filtre assignee
- **THEN** le système recharge le dashboard en affichant uniquement les deals assignés à ce commercial

#### Scenario: Liste dynamique des commerciaux
- **WHEN** la sidebar est affichée
- **THEN** le système liste uniquement les commerciaux présents dans la base de données

### Requirement: Date range filter
Le système SHALL permettre de filtrer les deals par plage de dates d'échéance via deux champs date.

#### Scenario: Filtrage par date de début
- **WHEN** l'utilisateur sélectionne une date de début dans le champ "Du"
- **THEN** le système affiche uniquement les deals avec une date d'échéance >= date de début

#### Scenario: Filtrage par plage complète
- **WHEN** l'utilisateur sélectionne une date de début et une date de fin
- **THEN** le système affiche uniquement les deals avec une date d'échéance entre les deux dates incluses

#### Scenario: Champs date vides
- **WHEN** les deux champs date sont vides
- **THEN** le système n'applique aucun filtre de date

### Requirement: Text search filter
Le système SHALL permettre de rechercher des deals par texte libre sur les champs client et notes.

#### Scenario: Recherche textuelle
- **WHEN** l'utilisateur saisit "Acme" dans le champ de recherche
- **THEN** le système affiche uniquement les deals dont le client ou les notes contiennent "Acme" (insensible à la casse)

#### Scenario: Recherche vide
- **WHEN** le champ de recherche est vide
- **THEN** le système n'applique aucun filtre textuel

### Requirement: Filter persistence via localStorage
Le système SHALL persister les filtres actifs dans le localStorage du navigateur.

#### Scenario: Sauvegarde des filtres
- **WHEN** l'utilisateur modifie un filtre
- **THEN** le système sauvegarde immédiatement l'état complet des filtres dans localStorage

#### Scenario: Restauration des filtres au chargement
- **WHEN** le dashboard est chargé et des filtres sont présents dans localStorage
- **THEN** le système restaure les filtres et affiche le dashboard filtré

#### Scenario: Pas de filtres sauvegardés
- **WHEN** le dashboard est chargé et aucun filtre n'est dans localStorage
- **THEN** le système affiche le dashboard sans filtres (toutes les données)

### Requirement: Reset filters button
Le système SHALL fournir un bouton "Réinitialiser les filtres" qui supprime tous les filtres actifs.

#### Scenario: Réinitialisation des filtres
- **WHEN** l'utilisateur clique sur "Réinitialiser les filtres"
- **THEN** le système décoche toutes les checkboxes, vide les champs date et recherche, supprime les filtres du localStorage, et recharge le dashboard complet

### Requirement: Global filter application
Le système SHALL appliquer les filtres de manière globale à toutes les sections du dashboard.

#### Scenario: Filtres appliqués aux KPIs
- **WHEN** des filtres sont actifs
- **THEN** les KPIs (pipeline pondéré, panier moyen, nb deals, taux conversion) sont recalculés sur le sous-ensemble filtré

#### Scenario: Filtres appliqués aux graphiques
- **WHEN** des filtres sont actifs
- **THEN** les graphiques secteurs et performance sont recalculés sur le sous-ensemble filtré

#### Scenario: Filtres appliqués aux tableaux
- **WHEN** des filtres sont actifs
- **THEN** les tableaux (deals, échéances, performance) affichent uniquement les données filtrées

#### Scenario: Combinaison de filtres
- **WHEN** l'utilisateur applique un filtre statut "Négociation" ET un filtre secteur "Tech"
- **THEN** le système affiche uniquement les deals en Négociation du secteur Tech (intersection des filtres)
