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

- [x] 3.1 Créer api/deals.py blueprint
- [x] 3.2 Implémenter GET /api/deals utilisant database/crud.py::get_all_deals()
- [x] 3.3 Implémenter DELETE /api/deals utilisant database/crud.py::clear_all_deals()
- [x] 3.4 Ajouter gestion d'erreurs avec format JSON {success, data, error}

## 4. API KPIs

- [x] 4.1 Créer api/analytics.py blueprint
- [x] 4.2 Implémenter GET /api/kpis calculant pipeline pondéré avec business_logic/calculators.py
- [x] 4.3 Implémenter calcul panier moyen (mean de montant_brut)
- [x] 4.4 Implémenter calcul nombre de deals et deals gagnés
- [x] 4.5 Implémenter calcul taux de conversion
- [x] 4.6 Formater montants avec utils/formatters.py::format_currency()

## 5. API Analytics Secteurs

- [x] 5.1 Implémenter GET /api/analytics/sectors dans api/analytics.py
- [x] 5.2 Calculer montants totaux par secteur (groupby + sum)
- [x] 5.3 Calculer paniers moyens par secteur (groupby + mean)
- [x] 5.4 Calculer top 5 secteurs par panier moyen (sort + head(5))
- [x] 5.5 Générer tableau récapitulatif avec toutes métriques par secteur
- [x] 5.6 Formater données pour Chart.js (labels + datasets)

## 6. API Analytics Échéances

- [x] 6.1 Implémenter GET /api/analytics/deadlines dans api/analytics.py
- [x] 6.2 Filtrer deals en retard (date_echeance < aujourd'hui)
- [x] 6.3 Calculer jours de retard pour chaque deal en retard
- [x] 6.4 Filtrer deals à venir (aujourd'hui <= date_echeance <= +30j)
- [x] 6.5 Calculer jours restants pour chaque deal à venir
- [x] 6.6 Générer statistiques (nb_overdue, nb_upcoming, montant_upcoming)
- [x] 6.7 Trier deals en retard par date croissante (plus urgent en premier)

## 7. API Upload CSV

- [x] 7.1 Créer api/upload.py blueprint
- [x] 7.2 Implémenter POST /api/upload/csv acceptant multipart/form-data
- [x] 7.3 Extraire fichier via request.files['file']
- [x] 7.4 Valider type fichier (.csv) et taille (< 200MB)
- [x] 7.5 Lire CSV avec pandas.read_csv() depuis stream mémoire
- [x] 7.6 Réutiliser business_logic/validators.py pour validation colonnes
- [x] 7.7 Appeler database/crud.py::clear_all_deals() avant import
- [x] 7.8 Réutiliser business_logic/calculators.py pour probabilités
- [x] 7.9 Appeler database/crud.py::insert_deals() pour insertion batch
- [x] 7.10 Retourner JSON avec statistiques (nb imported, errors)

## 8. Template HTML Base

- [x] 8.1 Créer templates/base.html avec structure HTML5
- [x] 8.2 Ajouter Tailwind CSS 3.x via CDN dans <head>
- [x] 8.3 Ajouter Chart.js 4.4.0 via CDN dans <head>
- [x] 8.4 Définir blocks Jinja2 (title, styles, content, scripts)
- [x] 8.5 Créer header avec titre "📊 Dashboard CRM - Fondateur"
- [x] 8.6 Créer footer avec mention "Dashboard CRM MVP - Phase 1"
- [x] 8.7 Lier static/css/custom.css pour styles personnalisés

## 9. Page Dashboard HTML

- [x] 9.1 Créer templates/dashboard.html héritant de base.html
- [x] 9.2 Créer section KPIs avec 4 cards responsive (grid cols-1 md:cols-4)
- [x] 9.3 Créer card Pipeline Pondéré avec icône 💰
- [x] 9.4 Créer card Panier Moyen avec icône 🛒
- [x] 9.5 Créer card Nombre de Deals avec icône 📊
- [x] 9.6 Créer card Deals Gagnés avec icône 🏆
- [x] 9.7 Créer section "Analyse par Secteur" avec titre
- [x] 9.8 Créer container pour graphique montants totaux (canvas Chart.js)
- [x] 9.9 Créer container pour graphique top 5 paniers moyens (canvas Chart.js)
- [x] 9.10 Créer table HTML pour tableau récapitulatif secteurs
- [x] 9.11 Créer section "Gestion des Échéances" avec titre
- [x] 9.12 Créer table HTML pour échéances dépassées
- [x] 9.13 Créer table HTML pour échéances à venir (30j)
- [x] 9.14 Créer section upload CSV avec zone drag & drop

## 10. JavaScript Client API

- [x] 10.1 Créer static/js/api.js avec fonctions fetch pour tous endpoints
- [x] 10.2 Implémenter fetchDeals() appelant GET /api/deals
- [x] 10.3 Implémenter fetchKPIs() appelant GET /api/kpis
- [x] 10.4 Implémenter fetchSectorAnalytics() appelant GET /api/analytics/sectors
- [x] 10.5 Implémenter fetchDeadlines() appelant GET /api/analytics/deadlines
- [x] 10.6 Implémenter uploadCSV(file) appelant POST /api/upload/csv avec FormData
- [x] 10.7 Ajouter gestion d'erreurs avec try/catch et messages utilisateur

## 11. JavaScript KPIs

- [x] 11.1 Créer static/js/main.js avec fonction loadKPIs()
- [x] 11.2 Appeler fetchKPIs() et récupérer données
- [x] 11.3 Injecter pipeline pondéré dans card DOM
- [x] 11.4 Injecter panier moyen dans card DOM
- [x] 11.5 Injecter nombre de deals dans card DOM
- [x] 11.6 Injecter deals gagnés et taux conversion dans card DOM
- [x] 11.7 Formater montants avec séparateurs milliers et symbole €

## 12. JavaScript Graphiques Chart.js

- [x] 12.1 Créer static/js/charts.js avec fonction initSectorCharts()
- [x] 12.2 Appeler fetchSectorAnalytics() et récupérer données
- [x] 12.3 Créer graphique Chart.js barres horizontales pour montants totaux
- [x] 12.4 Configurer palette bleus pour montants totaux
- [x] 12.5 Ajouter tooltips personnalisés avec formatage €
- [x] 12.6 Créer graphique Chart.js barres horizontales pour top 5 paniers moyens
- [x] 12.7 Configurer palette verts pour paniers moyens
- [x] 12.8 Ajouter animations d'apparition (800ms duration)
- [x] 12.9 Assurer labels secteurs complets et lisibles (pas de troncature)

## 13. JavaScript Tableau Secteurs

- [x] 13.1 Créer fonction renderSectorTable() dans charts.js
- [x] 13.2 Générer lignes HTML avec données secteurs (Secteur, Montant Total, Panier Moyen, Nb Deals, Valeur Pondérée)
- [x] 13.3 Formater tous montants avec séparateurs et €
- [x] 13.4 Trier secteurs par montant total décroissant
- [x] 13.5 Injecter HTML dans table DOM

## 14. JavaScript Échéances

- [x] 14.1 Créer fonction loadDeadlines() dans main.js
- [x] 14.2 Appeler fetchDeadlines() et récupérer données
- [x] 14.3 Générer lignes HTML pour tableau échéances dépassées
- [x] 14.4 Ajouter colonne jours de retard pour deals en retard
- [x] 14.5 Afficher alerte rouge si deals en retard existent
- [x] 14.6 Générer lignes HTML pour tableau échéances à venir (30j)
- [x] 14.7 Ajouter colonne jours restants pour deals à venir
- [x] 14.8 Formater dates en DD/MM/YYYY

## 15. JavaScript Upload CSV

- [x] 15.1 Créer static/js/upload.js avec gestion upload
- [x] 15.2 Implémenter zone drag & drop avec événements dragover, dragleave, drop
- [x] 15.3 Implémenter sélection fichier via input type="file" bouton "Parcourir"
- [x] 15.4 Valider type fichier .csv côté client
- [x] 15.5 Valider taille fichier < 200MB côté client
- [x] 15.6 Afficher nom fichier sélectionné
- [x] 15.7 Créer FormData et appeler uploadCSV() au clic bouton upload
- [x] 15.8 Afficher spinner pendant upload (désactiver bouton)
- [x] 15.9 Afficher message succès vert avec nb deals importés
- [x] 15.10 Afficher message erreur rouge si échec
- [x] 15.11 Rafraîchir automatiquement KPIs et graphiques après succès

## 16. Styles CSS Personnalisés

- [x] 16.1 Créer static/css/custom.css
- [x] 16.2 Ajouter styles hover pour cards KPIs (shadow transition 200ms)
- [x] 16.3 Ajouter styles zone drag & drop (bordure bleue au hover)
- [x] 16.4 Ajouter animations entrance pour graphiques (fade-in)
- [x] 16.5 Ajouter styles tables HTML (bordures, padding, hover rows)
- [x] 16.6 Assurer responsive design (breakpoints mobile < 640px)

## 17. Route Flask Dashboard

- [x] 17.1 Créer route GET / dans app.py
- [x] 17.2 Rendre templates/dashboard.html avec render_template()
- [x] 17.3 Tester accès http://localhost:5000/

## 18. Tests Manuels & Validation

- [x] 18.1 Tester lancement Flask avec `python app.py`
- [x] 18.2 Tester chargement page dashboard (http://localhost:5000/)
- [x] 18.3 Tester upload CSV avec fichier crm_prospects_demo.csv
- [x] 18.4 Vérifier affichage 4 KPIs avec valeurs correctes
- [x] 18.5 Vérifier graphique montants secteurs (22 secteurs, labels lisibles)
- [x] 18.6 Vérifier graphique top 5 paniers moyens
- [x] 18.7 Vérifier tableau récapitulatif secteurs (toutes colonnes)
- [x] 18.8 Vérifier tableau échéances dépassées (18 deals en retard)
- [x] 18.9 Vérifier tableau échéances à venir (vide si aucune dans 30j)
- [x] 18.10 Tester responsive mobile (simulateur Chrome DevTools)
- [x] 18.11 Tester drag & drop fichier CSV
- [x] 18.12 Tester messages erreur (fichier non CSV, trop volumineux)

## 19. Documentation & Finalisation

- [x] 19.1 Mettre à jour README.md avec instructions lancement Flask
- [x] 19.2 Documenter endpoints API dans README.md
- [x] 19.3 Archiver ancien code Streamlit dans archive/streamlit-old/
- [x] 19.4 Prendre screenshots du nouveau dashboard
- [x] 19.5 Créer commit Git avec message descriptif
- [ ] 19.6 Merge branche migration-flask dans main après validation
