## 1. Backend - Fonctions CRUD individuelles (database/crud.py)

- [x] 1.1 Ajouter la fonction `get_deal_by_id(deal_id)` qui retourne un dict du deal ou None si inexistant
- [x] 1.2 Ajouter la fonction `insert_deal(deal_dict)` qui insère un deal unique et retourne le deal créé avec son id
- [x] 1.3 Ajouter la fonction `update_deal(deal_id, deal_dict)` qui met à jour un deal existant et retourne le deal modifié
- [x] 1.4 Ajouter la fonction `delete_deal(deal_id)` qui supprime un deal individuel et retourne True/False

## 2. Backend - Filtrage en base de données (database/crud.py)

- [x] 2.1 Ajouter la fonction `get_filtered_deals(params)` qui construit dynamiquement les clauses WHERE avec paramètres liés (statut, secteur, assignee, date_from, date_to, search)
- [x] 2.2 Ajouter la fonction `get_filter_options()` qui retourne les listes distinctes de statuts, secteurs et assignees présents en base

## 3. Backend - Validation formulaire deal (business_logic/validators.py)

- [x] 3.1 Ajouter la fonction `validate_deal_dict(data)` qui valide un dict de deal (client non vide, statut valide, montant > 0, date valide si présente) et retourne (is_valid, errors)

## 4. Backend - Calculs performance commerciale (business_logic/calculators.py)

- [x] 4.1 Ajouter la fonction `calculate_performance_by_assignee(df)` qui retourne pour chaque assignee : nb_deals, montant_total, pipeline_pondere, deals_gagnes, taux_conversion, panier_moyen

## 5. Backend - Endpoints API deals CRUD (api/deals.py)

- [x] 5.1 Ajouter la route `POST /api/deals` : validation via validate_deal_dict, calcul probabilité/pondération via calculators, insertion via insert_deal, retour HTTP 201
- [x] 5.2 Ajouter la route `PUT /api/deals/<int:deal_id>` : vérification existence, validation, recalcul probabilité/pondération, update, retour HTTP 200
- [x] 5.3 Ajouter la route `DELETE /api/deals/<int:deal_id>` : vérification existence, suppression, retour HTTP 200 ou 404

## 6. Backend - Endpoint performance et options filtres (api/analytics.py)

- [x] 6.1 Ajouter la route `GET /api/analytics/performance` : appel calculate_performance_by_assignee, formatage Chart.js compatible, support query params filtres
- [x] 6.2 Ajouter la route `GET /api/filters/options` dans un nouveau blueprint ou dans analytics : retourne statuts, secteurs, assignees distincts via get_filter_options()

## 7. Backend - Intégration filtrage sur endpoints existants

- [x] 7.1 Modifier `GET /api/deals` pour accepter les query params (statut, secteur, assignee, date_from, date_to, search) et appeler get_filtered_deals au lieu de get_all_deals
- [x] 7.2 Modifier `GET /api/kpis` pour accepter les query params de filtrage et calculer les KPIs sur le sous-ensemble filtré
- [x] 7.3 Modifier `GET /api/analytics/sectors` pour accepter les query params de filtrage
- [x] 7.4 Modifier `GET /api/analytics/deadlines` pour accepter les query params de filtrage

## 8. Frontend - Layout sidebar (templates/base.html)

- [x] 8.1 Modifier base.html pour ajouter un layout 2 colonnes (sidebar 250px à gauche + contenu principal à droite) avec classes Tailwind responsive
- [x] 8.2 Ajouter un bouton hamburger dans le header, visible uniquement sur mobile (< 1024px), pour toggle la sidebar en overlay
- [x] 8.3 Ajouter un block Jinja2 `{% block sidebar %}` dans base.html pour le contenu de la sidebar

## 9. Frontend - Sidebar filtres (templates/dashboard.html + static/js/filters.js)

- [x] 9.1 Ajouter le HTML de la sidebar dans dashboard.html : sections checkboxes statut, secteur, assignee + champs date du/au + champ recherche texte + bouton réinitialiser
- [x] 9.2 Créer `static/js/filters.js` : charger les options via GET /api/filters/options, peupler dynamiquement les checkboxes
- [x] 9.3 Implémenter dans filters.js la construction de la query string à partir des filtres sélectionnés
- [x] 9.4 Implémenter la sauvegarde/restauration des filtres dans localStorage
- [x] 9.5 Implémenter le bouton réinitialiser : vider localStorage, décocher toutes les checkboxes, vider les champs, rafraîchir le dashboard

## 10. Frontend - Extension api.js pour les filtres et le CRUD

- [x] 10.1 Modifier toutes les fonctions fetch dans api.js (fetchDeals, fetchKPIs, fetchSectorAnalytics, fetchDeadlines) pour accepter un objet filters optionnel et construire la query string
- [x] 10.2 Ajouter la fonction `createDeal(data)` : POST /api/deals avec JSON body
- [x] 10.3 Ajouter la fonction `updateDeal(id, data)` : PUT /api/deals/<id> avec JSON body
- [x] 10.4 Ajouter la fonction `deleteDeal(id)` : DELETE /api/deals/<id>
- [x] 10.5 Ajouter la fonction `fetchPerformance(filters)` : GET /api/analytics/performance avec query params
- [x] 10.6 Ajouter la fonction `fetchFilterOptions()` : GET /api/filters/options

## 11. Frontend - Tableau des deals (templates/dashboard.html + static/js/main.js)

- [x] 11.1 Ajouter le HTML de la section "Liste des Deals" dans dashboard.html entre les KPIs et l'analyse secteurs, avec bouton "+ Nouveau Deal" et tableau (Client, Statut, Montant, Secteur, Assignee, Échéance, Actions)
- [x] 11.2 Ajouter dans main.js la fonction `loadDealsTable(filters)` qui appelle fetchDeals et peuple le tableau avec badges statut colorés et boutons Modifier/Supprimer
- [x] 11.3 Intégrer `loadDealsTable` dans `refreshDashboard()` pour qu'il soit rechargé avec les filtres actifs

## 12. Frontend - Modal formulaire deal (templates/dashboard.html + static/js/deal-form.js)

- [x] 12.1 Ajouter le HTML du modal dans dashboard.html : backdrop, conteneur centré, titre dynamique, formulaire (7 champs : client, statut select, montant, secteur, date échéance, assignee, notes textarea), boutons Annuler/Enregistrer
- [x] 12.2 Créer `static/js/deal-form.js` : fonctions openModal(mode, dealData), closeModal(), handleSubmit()
- [x] 12.3 Implémenter la validation côté client dans deal-form.js : champs requis, montant > 0, utiliser reportValidity() HTML5
- [x] 12.4 Implémenter la soumission : POST pour création, PUT pour édition, gestion des erreurs serveur, fermeture modal et refreshDashboard() en cas de succès
- [x] 12.5 Implémenter la suppression avec confirm() : appel deleteDeal(id) puis refreshDashboard()
- [x] 12.6 Implémenter les 3 modes de fermeture du modal : bouton X, clic backdrop, touche Escape

## 13. Frontend - Section performance commerciale (templates/dashboard.html + static/js/performance.js)

- [x] 13.1 Ajouter le HTML de la section "Performance Commerciale" dans dashboard.html entre les secteurs et les échéances : titre h2, canvas pour chart, tableau récapitulatif
- [x] 13.2 Créer `static/js/performance.js` : fonction `initPerformanceChart(filters)` qui appelle fetchPerformance et crée un chart barres groupées Chart.js (nb deals bleu + taux conversion vert)
- [x] 13.3 Ajouter dans performance.js la fonction `renderPerformanceTable(data)` qui peuple le tableau récapitulatif avec formatage (euros, pourcentages)
- [x] 13.4 Intégrer `initPerformanceChart` dans `refreshDashboard()` avec support des filtres

## 14. Frontend - Intégration globale (main.js + dashboard.html)

- [x] 14.1 Modifier `refreshDashboard()` dans main.js pour accepter un objet filters et le passer à toutes les fonctions de chargement (loadKPIs, initSectorCharts, loadDeadlines, loadDealsTable, initPerformanceChart)
- [x] 14.2 Ajouter les balises script dans dashboard.html pour les nouveaux fichiers JS : deal-form.js, filters.js, performance.js
- [x] 14.3 Modifier l'initialisation DOMContentLoaded pour restaurer les filtres depuis localStorage puis appeler refreshDashboard(filtresRestaurés)

## 15. Styles CSS (static/css/custom.css)

- [x] 15.1 Ajouter les styles du modal : backdrop semi-transparent, animation fadeIn, conteneur centré responsive
- [x] 15.2 Ajouter les styles de la sidebar : largeur fixe desktop, overlay mobile, transition slide-in
- [x] 15.3 Ajouter les styles des badges statut colorés : bleu Prospect, jaune Qualifié, orange Négociation, vert Gagné
- [x] 15.4 Ajouter les styles des boutons action dans le tableau des deals (modifier, supprimer)

## 16. Mise à jour footer et header

- [x] 16.1 Mettre à jour le footer dans base.html : remplacer "Phase 1" par "Phase 2 - V1"

## 17. Tests Playwright

- [x] 17.1 Tester le formulaire de création de deal : ouverture modal, remplissage champs, soumission, vérification dans le tableau
- [x] 17.2 Tester la modification d'un deal : clic Modifier, vérification pré-remplissage, modification, sauvegarde
- [x] 17.3 Tester la suppression d'un deal : clic Supprimer, confirmation, vérification disparition
- [x] 17.4 Tester les filtres : sélection d'un filtre statut, vérification mise à jour KPIs et tableau
- [x] 17.5 Tester la section performance commerciale : vérification affichage graphique et tableau
- [x] 17.6 Tester la responsivité : vérification sidebar collapsible, modal mobile, tableau scrollable
