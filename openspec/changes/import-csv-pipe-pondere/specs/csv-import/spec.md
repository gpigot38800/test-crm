## Purpose

Permettre l'import de données prospects depuis un fichier CSV via une interface Streamlit, avec parsing automatique, validation des données et insertion en base de données SQLite.

## ADDED Requirements

### Requirement: CSV File Upload Interface
Le système DOIT fournir une interface Streamlit permettant à l'utilisateur d'uploader un fichier CSV.

#### Scenario: Successful file upload
- **WHEN** l'utilisateur clique sur le bouton d'upload et sélectionne un fichier CSV valide
- **THEN** le système accepte le fichier et affiche le nom du fichier uploadé

#### Scenario: Invalid file type
- **WHEN** l'utilisateur tente d'uploader un fichier non-CSV (ex: .xlsx, .txt)
- **THEN** le système rejette le fichier et affiche un message d'erreur "Format de fichier non supporté. Veuillez uploader un fichier .csv"

### Requirement: CSV Structure Validation
Le système DOIT valider la structure du fichier CSV avant toute insertion en base de données.

#### Scenario: Valid CSV structure
- **WHEN** le fichier CSV contient toutes les colonnes requises (client, statut, montant_brut)
- **THEN** le système passe à l'étape de validation des données

#### Scenario: Missing required columns
- **WHEN** le fichier CSV ne contient pas une ou plusieurs colonnes requises
- **THEN** le système arrête l'import et affiche un message d'erreur listant les colonnes manquantes

#### Scenario: Empty CSV file
- **WHEN** le fichier CSV est vide ou ne contient que des headers
- **THEN** le système affiche un message d'erreur "Le fichier CSV ne contient aucune donnée"

### Requirement: Business Logic Validation
Le système DOIT valider chaque ligne du CSV selon les règles métier avant insertion.

#### Scenario: Valid deal row
- **WHEN** une ligne contient client non vide, statut valide (Prospect/Qualifié/Négociation/Gagné), et montant_brut positif
- **THEN** le système accepte la ligne pour insertion

#### Scenario: Invalid amount
- **WHEN** une ligne contient un montant_brut négatif ou nul
- **THEN** le système rejette la ligne et la signale dans le rapport d'erreurs

#### Scenario: Invalid status
- **WHEN** une ligne contient un statut non reconnu (ex: "En attente", "Perdu")
- **THEN** le système rejette la ligne et la signale dans le rapport d'erreurs avec message "Statut invalide. Valeurs acceptées: Prospect, Qualifié, Négociation, Gagné"

#### Scenario: Empty client name
- **WHEN** une ligne contient un champ client vide ou contenant uniquement des espaces
- **THEN** le système rejette la ligne et la signale dans le rapport d'erreurs

#### Scenario: Invalid date format
- **WHEN** une ligne contient une date_echeance dans un format non parsable
- **THEN** le système rejette la ligne et la signale dans le rapport d'erreurs avec message "Format de date invalide. Formats acceptés: YYYY-MM-DD, DD/MM/YYYY"

### Requirement: Column Mapping
Le système DOIT mapper automatiquement les colonnes du CSV vers le schéma de la table deals.

#### Scenario: Standard column names
- **WHEN** le CSV contient des colonnes nommées "Client", "Statut", "Montant", "Tags", "Date Échéance", "Assignee", "Notes"
- **THEN** le système mappe automatiquement vers client, statut, montant_brut, secteur, date_echeance, assignee, notes

#### Scenario: Case insensitive mapping
- **WHEN** le CSV contient des colonnes avec différentes casses (ex: "CLIENT", "client", "Client")
- **THEN** le système normalise les noms en minuscules avant mapping

#### Scenario: Optional columns missing
- **WHEN** le CSV ne contient pas les colonnes optionnelles (secteur, date_echeance, assignee, notes)
- **THEN** le système insère NULL pour ces champs et continue l'import

### Requirement: Data Insertion
Le système DOIT insérer les données validées dans la table deals de la base SQLite.

#### Scenario: Successful batch insert
- **WHEN** toutes les lignes du CSV sont valides
- **THEN** le système insère toutes les lignes en une seule transaction et affiche "X deals importés avec succès"

#### Scenario: Partial import with errors
- **WHEN** le CSV contient 10 lignes dont 2 invalides
- **THEN** le système insère les 8 lignes valides et affiche "8/10 deals importés. 2 lignes rejetées. Voir détails ci-dessous"

#### Scenario: Pre-import table clearing
- **WHEN** l'utilisateur lance un import
- **THEN** le système efface toutes les données existantes de la table deals avant insertion (TRUNCATE)

### Requirement: Import Feedback
Le système DOIT fournir un feedback détaillé sur le résultat de l'import.

#### Scenario: Successful import summary
- **WHEN** l'import se termine avec succès
- **THEN** le système affiche un message vert "Import réussi: X deals importés" avec la possibilité de consulter les données

#### Scenario: Error report display
- **WHEN** des lignes sont rejetées pendant l'import
- **THEN** le système affiche un tableau récapitulatif avec numéro de ligne, champ en erreur et message d'erreur détaillé

#### Scenario: Import progress indicator
- **WHEN** l'import est en cours (> 100 lignes)
- **THEN** le système affiche une barre de progression Streamlit indiquant le pourcentage de lignes traitées

### Requirement: Encoding Support
Le système DOIT supporter les encodages UTF-8 et Latin-1 pour les fichiers CSV contenant des caractères français.

#### Scenario: UTF-8 encoded file
- **WHEN** le fichier CSV est encodé en UTF-8 avec BOM et contient des caractères accentués (é, è, à)
- **THEN** le système parse correctement tous les caractères spéciaux

#### Scenario: Latin-1 fallback
- **WHEN** le fichier CSV échoue au parsing UTF-8
- **THEN** le système tente automatiquement le parsing en Latin-1 et affiche un avertissement "Fichier encodé en Latin-1 détecté"

#### Scenario: Unreadable encoding
- **WHEN** le fichier ne peut être parsé ni en UTF-8 ni en Latin-1
- **THEN** le système affiche un message d'erreur "Impossible de lire le fichier. Veuillez vérifier l'encodage"
