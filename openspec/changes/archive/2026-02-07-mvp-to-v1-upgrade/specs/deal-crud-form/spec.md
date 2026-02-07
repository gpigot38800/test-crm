## ADDED Requirements

### Requirement: Modal form for deal creation
Le système SHALL afficher un formulaire modal permettant de créer un nouveau deal avec les champs : client (texte, requis), statut (select parmi Prospect/Qualifié/Négociation/Gagné, requis), montant brut (nombre > 0, requis), secteur (texte, optionnel), date d'échéance (date, optionnel), assignee (texte, optionnel), notes (textarea, optionnel).

#### Scenario: Ouverture du modal de création
- **WHEN** l'utilisateur clique sur le bouton "+ Nouveau Deal"
- **THEN** le système affiche un modal overlay avec un formulaire vierge et le titre "Nouveau Deal"

#### Scenario: Création réussie d'un deal
- **WHEN** l'utilisateur remplit les champs requis (client, statut, montant) et clique "Enregistrer"
- **THEN** le système envoie POST /api/deals, ferme le modal, et rafraîchit le dashboard avec les données mises à jour

#### Scenario: Validation côté client - champs requis manquants
- **WHEN** l'utilisateur clique "Enregistrer" sans remplir les champs requis
- **THEN** le système affiche les messages de validation HTML5 natifs et ne soumet pas le formulaire

#### Scenario: Validation côté client - montant invalide
- **WHEN** l'utilisateur saisit un montant <= 0 ou non numérique
- **THEN** le système affiche un message d'erreur sous le champ montant et ne soumet pas le formulaire

### Requirement: Modal form for deal editing
Le système SHALL permettre de modifier un deal existant en pré-remplissant le modal avec ses données actuelles.

#### Scenario: Ouverture du modal d'édition
- **WHEN** l'utilisateur clique sur le bouton "Modifier" d'un deal dans le tableau
- **THEN** le système affiche le modal pré-rempli avec les données du deal et le titre "Modifier le Deal"

#### Scenario: Modification réussie d'un deal
- **WHEN** l'utilisateur modifie les champs et clique "Enregistrer"
- **THEN** le système envoie PUT /api/deals/<id>, ferme le modal, et rafraîchit le dashboard

#### Scenario: Calcul automatique des probabilités à l'édition
- **WHEN** l'utilisateur change le statut d'un deal dans le formulaire
- **THEN** le système recalcule automatiquement la probabilité et la valeur pondérée côté serveur lors de la sauvegarde

### Requirement: Deal deletion with confirmation
Le système SHALL permettre de supprimer un deal individuel avec une étape de confirmation.

#### Scenario: Demande de suppression
- **WHEN** l'utilisateur clique sur le bouton "Supprimer" d'un deal dans le tableau
- **THEN** le système affiche une boîte de dialogue de confirmation avec le nom du client et le montant

#### Scenario: Confirmation de suppression
- **WHEN** l'utilisateur confirme la suppression dans la boîte de dialogue
- **THEN** le système envoie DELETE /api/deals/<id>, ferme la boîte, et rafraîchit le dashboard

#### Scenario: Annulation de suppression
- **WHEN** l'utilisateur annule dans la boîte de dialogue de confirmation
- **THEN** le système ferme la boîte sans supprimer le deal

### Requirement: Modal closure behavior
Le système SHALL permettre de fermer le modal par plusieurs moyens sans perdre la page en cours.

#### Scenario: Fermeture par bouton X
- **WHEN** l'utilisateur clique sur le bouton X du modal
- **THEN** le système ferme le modal sans sauvegarder

#### Scenario: Fermeture par clic sur le backdrop
- **WHEN** l'utilisateur clique en dehors du modal (sur le backdrop)
- **THEN** le système ferme le modal sans sauvegarder

#### Scenario: Fermeture par touche Escape
- **WHEN** l'utilisateur appuie sur la touche Escape
- **THEN** le système ferme le modal sans sauvegarder

### Requirement: Server-side deal validation
Le système SHALL valider les données du deal côté serveur avant insertion ou mise à jour en base.

#### Scenario: Validation serveur réussie
- **WHEN** le serveur reçoit un POST ou PUT avec des données valides (client non vide, statut valide, montant > 0)
- **THEN** le système insère ou met à jour le deal et retourne HTTP 200/201 avec les données du deal créé/modifié

#### Scenario: Validation serveur échouée
- **WHEN** le serveur reçoit des données invalides (client vide, statut inconnu, ou montant <= 0)
- **THEN** le système retourne HTTP 400 avec un JSON {success: false, error: "message détaillant les erreurs"}

#### Scenario: Deal inexistant lors de la modification
- **WHEN** le serveur reçoit PUT /api/deals/<id> avec un ID inexistant
- **THEN** le système retourne HTTP 404 avec un JSON {success: false, error: "Deal non trouvé"}

### Requirement: Deals list table with actions
Le système SHALL afficher un tableau listant tous les deals avec des colonnes d'information et des boutons d'action par ligne.

#### Scenario: Affichage du tableau des deals
- **WHEN** le dashboard est chargé et des deals existent en base
- **THEN** le système affiche un tableau avec colonnes : Client, Statut (badge coloré), Montant, Secteur, Assignee, Échéance, Actions (Modifier/Supprimer)

#### Scenario: Tableau vide
- **WHEN** le dashboard est chargé et aucun deal n'existe en base
- **THEN** le système affiche un message "Aucun deal. Importez un CSV ou créez un deal manuellement."

#### Scenario: Badge coloré par statut
- **WHEN** un deal est affiché dans le tableau
- **THEN** le système affiche le statut avec un badge coloré : bleu pour Prospect, jaune pour Qualifié, orange pour Négociation, vert pour Gagné
