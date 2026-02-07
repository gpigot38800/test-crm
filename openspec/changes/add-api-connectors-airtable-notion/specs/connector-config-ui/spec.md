## ADDED Requirements

### Requirement: Connector configuration page accessible from navigation
Le système SHALL fournir une page dédiée /connectors accessible depuis la navigation principale du dashboard.

#### Scenario: Accès à la page connecteurs
- **WHEN** l'utilisateur clique sur le lien "Connecteurs" dans la navigation principale
- **THEN** le système affiche la page /connectors avec les onglets Airtable et Notion

#### Scenario: Affichage responsive de la page
- **WHEN** l'utilisateur accède à la page /connectors sur mobile (viewport < 768px)
- **THEN** la page s'adapte avec les onglets empilés et les formulaires en pleine largeur

### Requirement: Connector configuration form per provider
Le système SHALL afficher un formulaire de configuration pour chaque connecteur avec les champs token, identifiant de base et nom de table.

#### Scenario: Formulaire Airtable
- **WHEN** l'utilisateur sélectionne l'onglet Airtable
- **THEN** le système affiche un formulaire avec les champs : API Token (type password), Base ID (type text), Table Name (type text), et un bouton "Sauvegarder"

#### Scenario: Formulaire Notion
- **WHEN** l'utilisateur sélectionne l'onglet Notion
- **THEN** le système affiche un formulaire avec les champs : Integration Token (type password), Database ID (type text), et un bouton "Sauvegarder"

#### Scenario: Chargement de la configuration existante
- **WHEN** la page se charge et qu'un connecteur a déjà une configuration en base
- **THEN** le système pré-remplit les champs base_id et table_name mais affiche le token masqué ("***") avec un placeholder "Entrez un nouveau token pour le modifier"

#### Scenario: Sauvegarde de la configuration
- **WHEN** l'utilisateur remplit le formulaire et clique "Sauvegarder"
- **THEN** le système envoie PUT /api/connectors/config/<provider> et affiche un message de confirmation "Configuration sauvegardée"

#### Scenario: Sauvegarde sans modifier le token
- **WHEN** l'utilisateur modifie base_id ou table_name sans toucher au champ token (reste "***")
- **THEN** le système envoie la requête PUT sans le champ api_token pour conserver le token existant en base

### Requirement: Field mapping configuration
Le système SHALL permettre à l'utilisateur de configurer le mapping entre les champs du service externe et les champs CRM.

#### Scenario: Affichage du mapping par défaut
- **WHEN** l'utilisateur ouvre la section mapping d'un connecteur sans configuration préalable
- **THEN** le système affiche le mapping par défaut avec les correspondances CRM → Service (client → Name, statut → Status, montant_brut → Amount, secteur → Sector, date_echeance → Due Date, assignee → Assignee, notes → Notes)

#### Scenario: Modification d'un mapping
- **WHEN** l'utilisateur modifie le nom d'un champ externe (ex: "Amount" → "Montant")
- **THEN** le système met à jour le mapping en mémoire et le sauvegarde avec la configuration lors du clic "Sauvegarder"

#### Scenario: Champs CRM non modifiables
- **WHEN** l'utilisateur consulte la section mapping
- **THEN** les noms des champs CRM (client, statut, montant_brut, etc.) sont affichés en lecture seule, seuls les noms des champs externes sont éditables

### Requirement: Test connection button
Le système SHALL fournir un bouton pour tester la connexion à chaque service externe avant la synchronisation.

#### Scenario: Test de connexion réussi
- **WHEN** l'utilisateur clique "Tester la connexion" et la configuration est valide
- **THEN** le système envoie POST /api/connectors/test/<provider> et affiche un badge vert "Connecté" avec le nombre de records disponibles

#### Scenario: Test de connexion échoué
- **WHEN** l'utilisateur clique "Tester la connexion" et le token ou l'identifiant est invalide
- **THEN** le système affiche un badge rouge "Erreur" avec le message d'erreur retourné par l'API

#### Scenario: Test de connexion sans configuration
- **WHEN** l'utilisateur clique "Tester la connexion" sans avoir rempli les champs requis
- **THEN** le système affiche un message d'avertissement "Veuillez remplir tous les champs requis avant de tester"

### Requirement: Import and export action buttons
Le système SHALL fournir des boutons pour déclencher manuellement l'import et l'export des deals.

#### Scenario: Déclenchement import
- **WHEN** l'utilisateur clique "Importer depuis Airtable" (ou Notion)
- **THEN** le système envoie POST /api/sync/<provider>/import, affiche un indicateur de chargement pendant l'opération, et affiche le résumé à la fin (X créés, Y mis à jour, Z erreurs)

#### Scenario: Déclenchement export
- **WHEN** l'utilisateur clique "Exporter vers Airtable" (ou Notion)
- **THEN** le système envoie POST /api/sync/<provider>/export, affiche un indicateur de chargement pendant l'opération, et affiche le résumé à la fin

#### Scenario: Boutons désactivés sans configuration
- **WHEN** la page se charge et qu'un connecteur n'a pas de configuration complète (token ou base_id manquant)
- **THEN** les boutons Import et Export sont désactivés avec un tooltip "Configurez d'abord le connecteur"

### Requirement: Sync logs display
Le système SHALL afficher l'historique des opérations de synchronisation.

#### Scenario: Affichage des logs récents
- **WHEN** la page connecteurs se charge
- **THEN** le système récupère GET /api/sync/logs et affiche un tableau avec les 20 dernières opérations : date, provider, direction (import/export), statut (succès/erreur/partiel), nombre de records traités

#### Scenario: Log vide
- **WHEN** aucune synchronisation n'a été effectuée
- **THEN** le système affiche un message "Aucune synchronisation effectuée pour le moment"

#### Scenario: Indicateur visuel du statut
- **WHEN** un log a le statut "success"
- **THEN** le système affiche un badge vert
- **WHEN** un log a le statut "error"
- **THEN** le système affiche un badge rouge avec le message d'erreur au survol
- **WHEN** un log a le statut "partial"
- **THEN** le système affiche un badge orange
