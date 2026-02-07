## ADDED Requirements

### Requirement: Interface HTML responsive avec Tailwind CSS
Le système SHALL fournir une interface HTML5 responsive utilisant Tailwind CSS via CDN pour un affichage optimal sur desktop, tablet et mobile.

#### Scenario: Affichage sur desktop
- **WHEN** l'interface est affichée sur un écran >= 1024px
- **THEN** le système affiche 4 colonnes de KPIs côte à côte

#### Scenario: Affichage sur mobile
- **WHEN** l'interface est affichée sur un écran < 640px
- **THEN** le système affiche les KPIs en pile verticale

#### Scenario: Chargement des styles
- **WHEN** la page dashboard est chargée
- **THEN** le système charge Tailwind CSS depuis CDN sans erreur

### Requirement: Séparation template base et contenu
Le système SHALL utiliser un template base.html avec blocks Jinja2 pour réutilisation et cohérence.

#### Scenario: Héritage de template
- **WHEN** dashboard.html est rendu
- **THEN** le système étend base.html et injecte le contenu dans les blocks appropriés

#### Scenario: Header et footer communs
- **WHEN** une page est affichée
- **THEN** le système affiche header et footer définis dans base.html

### Requirement: Affichage KPIs visuels
Le système SHALL afficher 4 KPIs en cards avec icônes, valeurs formatées et descriptions.

#### Scenario: Card Pipeline Pondéré
- **WHEN** le dashboard est affiché
- **THEN** le système affiche une card avec icône 💰, valeur en euros et libellé "Pipeline Pondéré Total"

#### Scenario: Card Panier Moyen
- **WHEN** le dashboard est affiché
- **THEN** le système affiche une card avec icône 🛒, valeur en euros et libellé "Panier Moyen"

#### Scenario: Card Nombre de Deals
- **WHEN** le dashboard est affiché
- **THEN** le système affiche une card avec icône 📊, nombre entier et libellé "Nombre de Deals"

#### Scenario: Card Deals Gagnés
- **WHEN** le dashboard est affiché
- **THEN** le système affiche une card avec icône 🏆, nombre et pourcentage de deals gagnés

### Requirement: Interface claire et minimaliste
Le système SHALL utiliser une interface claire sans mode sombre, avec fond blanc et typographie lisible.

#### Scenario: Palette de couleurs
- **WHEN** le dashboard est affiché
- **THEN** le système utilise un fond blanc avec texte gris foncé et accents bleus

#### Scenario: Pas de mode sombre
- **WHEN** l'utilisateur accède au dashboard
- **THEN** le système affiche uniquement le thème clair sans option de basculement
