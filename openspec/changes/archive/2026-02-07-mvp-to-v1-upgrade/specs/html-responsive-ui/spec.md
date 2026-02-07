## ADDED Requirements

### Requirement: Two-column layout with sidebar
Le système SHALL utiliser un layout 2 colonnes avec une sidebar de filtres à gauche et le contenu principal à droite.

#### Scenario: Layout desktop
- **WHEN** l'interface est affichée sur un écran >= 1024px
- **THEN** le système affiche une sidebar fixe de 250px à gauche contenant les filtres, et le contenu principal occupe l'espace restant à droite

#### Scenario: Layout mobile
- **WHEN** l'interface est affichée sur un écran < 1024px
- **THEN** le contenu principal occupe 100% de la largeur et la sidebar est accessible via un bouton hamburger dans le header

### Requirement: Hamburger menu button
Le système SHALL afficher un bouton hamburger dans le header sur les écrans mobiles pour ouvrir la sidebar.

#### Scenario: Visibilité du bouton hamburger
- **WHEN** l'interface est affichée sur un écran < 1024px
- **THEN** un bouton hamburger (3 barres horizontales) est visible dans le header à gauche du titre

#### Scenario: Bouton caché sur desktop
- **WHEN** l'interface est affichée sur un écran >= 1024px
- **THEN** le bouton hamburger est masqué car la sidebar est déjà visible

### Requirement: Deal form modal HTML structure
Le système SHALL intégrer le HTML du modal de formulaire deal dans le template dashboard.html.

#### Scenario: Structure HTML du modal
- **WHEN** le modal est affiché
- **THEN** le système affiche un backdrop semi-transparent, un conteneur centré avec titre, formulaire (7 champs), et boutons "Annuler" et "Enregistrer"

#### Scenario: Responsive modal
- **WHEN** le modal est affiché sur mobile (< 640px)
- **THEN** le modal occupe 95% de la largeur de l'écran avec marges réduites

### Requirement: Performance section HTML structure
Le système SHALL intégrer la section performance commerciale dans le template dashboard.html entre les secteurs et les échéances.

#### Scenario: Structure de la section performance
- **WHEN** le dashboard est affiché
- **THEN** la section "Performance Commerciale" contient un titre h2, un graphique canvas, et un tableau récapitulatif

#### Scenario: Grid responsive performance
- **WHEN** la section performance est affichée sur desktop (>= 1024px)
- **THEN** le graphique et le tableau sont côte à côte en 2 colonnes

### Requirement: Deals list section HTML structure
Le système SHALL intégrer un tableau de liste des deals dans le template dashboard.html entre les KPIs et l'analyse par secteur.

#### Scenario: Position du tableau deals
- **WHEN** le dashboard est affiché
- **THEN** la section "Liste des Deals" apparaît après les KPIs et avant l'analyse par secteur, avec un bouton "+ Nouveau Deal" en haut à droite du titre

#### Scenario: Tableau responsive
- **WHEN** le tableau des deals est affiché sur mobile
- **THEN** le tableau est scrollable horizontalement pour afficher toutes les colonnes

## MODIFIED Requirements

### Requirement: Interface HTML responsive avec Tailwind CSS
Le système SHALL fournir une interface HTML5 responsive utilisant Tailwind CSS via CDN avec un layout 2 colonnes (sidebar filtres + contenu principal) pour un affichage optimal sur desktop, tablet et mobile.

#### Scenario: Affichage sur desktop
- **WHEN** l'interface est affichée sur un écran >= 1024px
- **THEN** le système affiche la sidebar de filtres à gauche et 4 colonnes de KPIs côte à côte dans le contenu principal

#### Scenario: Affichage sur mobile
- **WHEN** l'interface est affichée sur un écran < 640px
- **THEN** le système masque la sidebar, affiche les KPIs en pile verticale, et propose un bouton hamburger pour accéder aux filtres

#### Scenario: Chargement des styles
- **WHEN** la page dashboard est chargée
- **THEN** le système charge Tailwind CSS depuis CDN sans erreur

### Requirement: Séparation template base et contenu
Le système SHALL utiliser un template base.html avec blocks Jinja2 pour réutilisation et cohérence, incluant le support du layout sidebar.

#### Scenario: Héritage de template
- **WHEN** dashboard.html est rendu
- **THEN** le système étend base.html et injecte le contenu dans les blocks appropriés

#### Scenario: Header et footer communs
- **WHEN** une page est affichée
- **THEN** le système affiche header (avec bouton hamburger mobile) et footer définis dans base.html

#### Scenario: Block sidebar
- **WHEN** dashboard.html est rendu
- **THEN** le système injecte la sidebar de filtres dans le block sidebar de base.html
