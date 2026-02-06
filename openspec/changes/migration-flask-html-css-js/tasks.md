## 1. Setup Infrastructure

- [x] 1.1 Créer nouvelle branche Git `migration-flask`
- [x] 1.2 Créer structure dossiers (api/, templates/, static/css/, static/js/, static/img/)
- [x] 1.3 Ajouter Flask 3.0 au requirements.txt
- [x] 1.4 Supprimer Streamlit et Plotly du requirements.txt
- [x] 1.5 Installer les nouvelles dépendances avec pip install

## 2. Backend Flask Core

- [x] 2.1 Créer app.py Flask avec configuration de base
- [x] 2.2 Créer api/__init__.py avec enregistrement des blueprints
- [x] 2.3 Configurer Flask debug mode et CORS si nécessaire

## 3. API Deals

- [ ] 3.1 Créer api/deals.py blueprint
- [ ] 3.2 Implémenter GET /api/deals utilisant database/crud.py::get_all_deals()
- [ ] 3.3 Implémenter DELETE /api/deals utilisant database/crud.py::clear_all_deals()
- [ ] 3.4 Ajouter gestion d'erreurs avec format JSON {success, data, error}

## 4. API KPIs

- [ ] 4.1 Créer api/analytics.py blueprint
- [ ] 4.2 Implémenter GET /api/kpis calculant pipeline pondéré avec business_logic/calculators.py
- [ ] 4.3 Implémenter calcul panier moyen (mean de montant_brut)
- [ ] 4.4 Implémenter calcul nombre de deals et deals gagnés
- [ ] 4.5 Implémenter calcul taux de conversion
- [ ] 4.6 Formater montants avec utils/formatters.py::format_currency()

## 5. API Analytics Secteurs

- [ ] 5.1 Implémenter GET /api/analytics/sectors dans api/analytics.py
- [ ] 5.2 Calculer montants totaux par secteur (groupby + sum)
- [ ] 5.3 Calculer paniers moyens par secteur (groupby + mean)
- [ ] 5.4 Calculer top 5 secteurs par panier moyen (sort + head(5))
- [ ] 5.5 Générer tableau récapitulatif avec toutes métriques par secteur
- [ ] 5.6 Formater données pour Chart.js (labels + datasets)

## 6. API Analytics Échéances

- [ ] 6.1 Implémenter GET /api/analytics/deadlines dans api/analytics.py
- [ ] 6.2 Filtrer deals en retard (date_echeance < aujourd'hui)
- [ ] 6.3 Calculer jours de retard pour chaque deal en retard
- [ ] 6.4 Filtrer deals à venir (aujourd'hui <= date_echeance <= +30j)
- [ ] 6.5 Calculer jours restants pour chaque deal à venir
- [ ] 6.6 Générer statistiques (nb_overdue, nb_upcoming, montant_upcoming)
- [ ] 6.7 Trier deals en retard par date croissante (plus urgent en premier)

## 7. API Upload CSV

- [ ] 7.1 Créer api/upload.py blueprint
- [ ] 7.2 Implémenter POST /api/upload/csv acceptant multipart/form-data
- [ ] 7.3 Extraire fichier via request.files['file']
- [ ] 7.4 Valider type fichier (.csv) et taille (< 200MB)
- [ ] 7.5 Lire CSV avec pandas.read_csv() depuis stream mémoire
- [ ] 7.6 Réutiliser business_logic/validators.py pour validation colonnes
- [ ] 7.7 Appeler database/crud.py::clear_all_deals() avant import
- [ ] 7.8 Réutiliser business_logic/calculators.py pour probabilités
- [ ] 7.9 Appeler database/crud.py::insert_deals() pour insertion batch
- [ ] 7.10 Retourner JSON avec statistiques (nb imported, errors)

## 8. Template HTML Base

- [ ] 8.1 Créer templates/base.html avec structure HTML5
- [ ] 8.2 Ajouter Tailwind CSS 3.x via CDN dans <head>
- [ ] 8.3 Ajouter Chart.js 4.4.0 via CDN dans <head>
- [ ] 8.4 Définir blocks Jinja2 (title, styles, content, scripts)
- [ ] 8.5 Créer header avec titre "📊 Dashboard CRM - Fondateur"
- [ ] 8.6 Créer footer avec mention "Dashboard CRM MVP - Phase 1"
- [ ] 8.7 Lier static/css/custom.css pour styles personnalisés

## 9. Page Dashboard HTML

- [ ] 9.1 Créer templates/dashboard.html héritant de base.html
- [ ] 9.2 Créer section KPIs avec 4 cards responsive (grid cols-1 md:cols-4)
- [ ] 9.3 Créer card Pipeline Pondéré avec icône 💰
- [ ] 9.4 Créer card Panier Moyen avec icône 🛒
- [ ] 9.5 Créer card Nombre de Deals avec icône 📊
- [ ] 9.6 Créer card Deals Gagnés avec icône 🏆
- [ ] 9.7 Créer section "Analyse par Secteur" avec titre
- [ ] 9.8 Créer container pour graphique montants totaux (canvas Chart.js)
- [ ] 9.9 Créer container pour graphique top 5 paniers moyens (canvas Chart.js)
- [ ] 9.10 Créer table HTML pour tableau récapitulatif secteurs
- [ ] 9.11 Créer section "Gestion des Échéances" avec titre
- [ ] 9.12 Créer table HTML pour échéances dépassées
- [ ] 9.13 Créer table HTML pour échéances à venir (30j)
- [ ] 9.14 Créer section upload CSV avec zone drag & drop

## 10. JavaScript Client API

- [ ] 10.1 Créer static/js/api.js avec fonctions fetch pour tous endpoints
- [ ] 10.2 Implémenter fetchDeals() appelant GET /api/deals
- [ ] 10.3 Implémenter fetchKPIs() appelant GET /api/kpis
- [ ] 10.4 Implémenter fetchSectorAnalytics() appelant GET /api/analytics/sectors
- [ ] 10.5 Implémenter fetchDeadlines() appelant GET /api/analytics/deadlines
- [ ] 10.6 Implémenter uploadCSV(file) appelant POST /api/upload/csv avec FormData
- [ ] 10.7 Ajouter gestion d'erreurs avec try/catch et messages utilisateur

## 11. JavaScript KPIs

- [ ] 11.1 Créer static/js/main.js avec fonction loadKPIs()
- [ ] 11.2 Appeler fetchKPIs() et récupérer données
- [ ] 11.3 Injecter pipeline pondéré dans card DOM
- [ ] 11.4 Injecter panier moyen dans card DOM
- [ ] 11.5 Injecter nombre de deals dans card DOM
- [ ] 11.6 Injecter deals gagnés et taux conversion dans card DOM
- [ ] 11.7 Formater montants avec séparateurs milliers et symbole €

## 12. JavaScript Graphiques Chart.js

- [ ] 12.1 Créer static/js/charts.js avec fonction initSectorCharts()
- [ ] 12.2 Appeler fetchSectorAnalytics() et récupérer données
- [ ] 12.3 Créer graphique Chart.js barres horizontales pour montants totaux
- [ ] 12.4 Configurer palette bleus pour montants totaux
- [ ] 12.5 Ajouter tooltips personnalisés avec formatage €
- [ ] 12.6 Créer graphique Chart.js barres horizontales pour top 5 paniers moyens
- [ ] 12.7 Configurer palette verts pour paniers moyens
- [ ] 12.8 Ajouter animations d'apparition (800ms duration)
- [ ] 12.9 Assurer labels secteurs complets et lisibles (pas de troncature)

## 13. JavaScript Tableau Secteurs

- [ ] 13.1 Créer fonction renderSectorTable() dans charts.js
- [ ] 13.2 Générer lignes HTML avec données secteurs (Secteur, Montant Total, Panier Moyen, Nb Deals, Valeur Pondérée)
- [ ] 13.3 Formater tous montants avec séparateurs et €
- [ ] 13.4 Trier secteurs par montant total décroissant
- [ ] 13.5 Injecter HTML dans table DOM

## 14. JavaScript Échéances

- [ ] 14.1 Créer fonction loadDeadlines() dans main.js
- [ ] 14.2 Appeler fetchDeadlines() et récupérer données
- [ ] 14.3 Générer lignes HTML pour tableau échéances dépassées
- [ ] 14.4 Ajouter colonne jours de retard pour deals en retard
- [ ] 14.5 Afficher alerte rouge si deals en retard existent
- [ ] 14.6 Générer lignes HTML pour tableau échéances à venir (30j)
- [ ] 14.7 Ajouter colonne jours restants pour deals à venir
- [ ] 14.8 Formater dates en DD/MM/YYYY

## 15. JavaScript Upload CSV

- [ ] 15.1 Créer static/js/upload.js avec gestion upload
- [ ] 15.2 Implémenter zone drag & drop avec événements dragover, dragleave, drop
- [ ] 15.3 Implémenter sélection fichier via input type="file" bouton "Parcourir"
- [ ] 15.4 Valider type fichier .csv côté client
- [ ] 15.5 Valider taille fichier < 200MB côté client
- [ ] 15.6 Afficher nom fichier sélectionné
- [ ] 15.7 Créer FormData et appeler uploadCSV() au clic bouton upload
- [ ] 15.8 Afficher spinner pendant upload (désactiver bouton)
- [ ] 15.9 Afficher message succès vert avec nb deals importés
- [ ] 15.10 Afficher message erreur rouge si échec
- [ ] 15.11 Rafraîchir automatiquement KPIs et graphiques après succès

## 16. Styles CSS Personnalisés

- [ ] 16.1 Créer static/css/custom.css
- [ ] 16.2 Ajouter styles hover pour cards KPIs (shadow transition 200ms)
- [ ] 16.3 Ajouter styles zone drag & drop (bordure bleue au hover)
- [ ] 16.4 Ajouter animations entrance pour graphiques (fade-in)
- [ ] 16.5 Ajouter styles tables HTML (bordures, padding, hover rows)
- [ ] 16.6 Assurer responsive design (breakpoints mobile < 640px)

## 17. Route Flask Dashboard

- [ ] 17.1 Créer route GET / dans app.py
- [ ] 17.2 Rendre templates/dashboard.html avec render_template()
- [ ] 17.3 Tester accès http://localhost:5000/

## 18. Tests Manuels & Validation

- [ ] 18.1 Tester lancement Flask avec `python app.py`
- [ ] 18.2 Tester chargement page dashboard (http://localhost:5000/)
- [ ] 18.3 Tester upload CSV avec fichier crm_prospects_demo.csv
- [ ] 18.4 Vérifier affichage 4 KPIs avec valeurs correctes
- [ ] 18.5 Vérifier graphique montants secteurs (22 secteurs, labels lisibles)
- [ ] 18.6 Vérifier graphique top 5 paniers moyens
- [ ] 18.7 Vérifier tableau récapitulatif secteurs (toutes colonnes)
- [ ] 18.8 Vérifier tableau échéances dépassées (18 deals en retard)
- [ ] 18.9 Vérifier tableau échéances à venir (vide si aucune dans 30j)
- [ ] 18.10 Tester responsive mobile (simulateur Chrome DevTools)
- [ ] 18.11 Tester drag & drop fichier CSV
- [ ] 18.12 Tester messages erreur (fichier non CSV, trop volumineux)

## 19. Documentation & Finalisation

- [ ] 19.1 Mettre à jour README.md avec instructions lancement Flask
- [ ] 19.2 Documenter endpoints API dans README.md
- [ ] 19.3 Archiver ancien code Streamlit dans archive/streamlit-old/
- [ ] 19.4 Prendre screenshots du nouveau dashboard
- [ ] 19.5 Créer commit Git avec message descriptif
- [ ] 19.6 Merge branche migration-flask dans main après validation
