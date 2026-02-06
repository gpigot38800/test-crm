## ADDED Requirements

### Requirement: Interface upload CSV avec drag & drop
Le système SHALL fournir une interface HTML pour uploader un fichier CSV avec support du drag & drop et sélection de fichier.

#### Scenario: Zone drag & drop visible
- **WHEN** le dashboard est affiché
- **THEN** le système affiche une zone délimitée avec icône et texte "Glissez votre fichier CSV ici"

#### Scenario: Drag & drop fichier CSV
- **WHEN** l'utilisateur glisse un fichier CSV sur la zone
- **THEN** le système change visuellement la zone (bordure bleue) pour indiquer la zone de drop

#### Scenario: Sélection fichier via bouton
- **WHEN** l'utilisateur clique sur le bouton "Parcourir"
- **THEN** le système ouvre le sélecteur de fichiers natif filtré sur .csv

#### Scenario: Prévisualisation nom fichier
- **WHEN** l'utilisateur sélectionne un fichier CSV
- **THEN** le système affiche le nom du fichier sélectionné dans l'interface

### Requirement: Validation fichier côté client
Le système SHALL valider le type et la taille du fichier CSV avant upload.

#### Scenario: Fichier non CSV rejeté
- **WHEN** l'utilisateur sélectionne un fichier non .csv
- **THEN** le système affiche un message d'erreur "Seuls les fichiers CSV sont acceptés" et refuse l'upload

#### Scenario: Fichier trop volumineux rejeté
- **WHEN** l'utilisateur sélectionne un fichier > 200MB
- **THEN** le système affiche un message d'erreur "Fichier trop volumineux (max 200MB)" et refuse l'upload

### Requirement: Upload asynchrone avec feedback
Le système SHALL uploader le fichier CSV de manière asynchrone avec indicateur de progression et messages de statut.

#### Scenario: Indicateur de chargement
- **WHEN** l'utilisateur lance l'upload d'un CSV
- **THEN** le système affiche un spinner et désactive le bouton d'upload

#### Scenario: Upload réussi
- **WHEN** l'upload et le traitement CSV se terminent avec succès
- **THEN** le système affiche un message de succès vert avec le nombre de deals importés

#### Scenario: Upload échoué
- **WHEN** l'upload ou le traitement CSV échoue
- **THEN** le système affiche un message d'erreur rouge avec détails de l'erreur

### Requirement: Endpoint POST /api/upload/csv
Le système SHALL exposer un endpoint POST /api/upload/csv acceptant multipart/form-data pour traiter le fichier CSV.

#### Scenario: Réception fichier CSV valide
- **WHEN** le serveur reçoit POST /api/upload/csv avec un fichier CSV valide
- **THEN** le système lit le fichier, valide les colonnes, calcule les probabilités et insère les deals en base

#### Scenario: Clear avant import
- **WHEN** le serveur démarre le traitement d'un nouveau CSV
- **THEN** le système supprime tous les deals existants avant l'insertion

#### Scenario: Réponse succès avec statistiques
- **WHEN** l'import CSV se termine avec succès
- **THEN** le système retourne HTTP 200 avec JSON {success: true, data: {imported: 22, errors: []}}

#### Scenario: Validation colonnes requises
- **WHEN** le CSV ne contient pas les colonnes Client, Statut ou Montant
- **THEN** le système retourne HTTP 400 avec JSON {success: false, error: "Colonnes manquantes: Client, Statut, Montant"}

### Requirement: Rafraîchissement automatique dashboard
Le système SHALL rafraîchir automatiquement les données du dashboard après un import CSV réussi.

#### Scenario: Rechargement KPIs après import
- **WHEN** l'upload CSV se termine avec succès
- **THEN** le système recharge automatiquement les KPIs via GET /api/kpis

#### Scenario: Rechargement graphiques après import
- **WHEN** l'upload CSV se termine avec succès
- **THEN** le système recharge automatiquement les graphiques via GET /api/analytics/sectors et /api/analytics/deadlines
