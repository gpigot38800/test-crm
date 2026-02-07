## 1. Constantes et configuration

- [x] 1.1 Ajouter la constante `COLD_DEAL_THRESHOLD_DAYS = 10` dans `utils/constants.py`

## 2. Business Logic — Fonctions de calcul

- [x] 2.1 Ajouter `calculate_sales_velocity(df)` dans `business_logic/calculators.py` : calcule la durée moyenne en jours (`updated_at - created_at`) pour les deals au statut "Gagné", retourne 0 si aucun deal gagné
- [x] 2.2 Ajouter `calculate_velocity_by_group(df, group_col)` dans `business_logic/calculators.py` : ventile la vitesse de vente par secteur ou commercial, retourne un dict {groupe: durée_moyenne_jours}
- [x] 2.3 Ajouter `get_cold_deals(df, threshold_days)` dans `business_logic/calculators.py` : filtre les deals dont `updated_at` > threshold_days et statut != "Gagné", retourne un DataFrame avec colonne `jours_inactifs`

## 3. Backend — Endpoint Vitesse de Vente

- [x] 3.1 Ajouter l'endpoint `GET /api/analytics/velocity` dans `api/analytics.py` retournant vitesse_moyenne_jours, velocity_by_sector et velocity_by_assignee au format JSON
- [x] 3.2 Supporter les paramètres de filtres existants (statut, secteur, assignee, dates) sur l'endpoint velocity

## 4. Backend — Endpoint Deals Froids

- [x] 4.1 Ajouter l'endpoint `GET /api/analytics/cold-deals` dans `api/analytics.py` retournant la liste des deals froids avec id, client, statut, montant_brut, secteur, assignee, jours_inactifs et les stats agrégées (nb_cold_deals, montant_total_cold)
- [x] 4.2 Supporter les paramètres de filtres existants sur l'endpoint cold-deals

## 5. Backend — Modification endpoint KPIs

- [x] 5.1 Étendre l'endpoint `GET /api/kpis` dans `api/analytics.py` pour inclure `vitesse_vente_moyenne`, `vitesse_vente_formatted` et `nb_cold_deals` dans la réponse JSON

## 6. Frontend — Section Vitesse de Vente

- [x] 6.1 Ajouter la section HTML "Vitesse de Vente" dans `templates/dashboard.html` avec un KPI principal (vitesse moyenne en jours) et un conteneur pour le graphique Chart.js
- [x] 6.2 Ajouter le JavaScript pour appeler `GET /api/analytics/velocity` et alimenter le KPI et le graphique barres horizontales par secteur
- [x] 6.3 Assurer le responsive mobile (< 768px) : section pleine largeur, graphique empilé sous le KPI

## 7. Frontend — Section Simulateur What-If

- [x] 7.1 Ajouter la section HTML "Simulateur What-If" dans `templates/dashboard.html` avec un curseur range (-50% à +50%, pas de 5%), affichage du pourcentage, nouveau panier moyen projeté, nouveau pipeline projeté et différence en € avec indicateur vert/rouge
- [x] 7.2 Ajouter le JavaScript pour le calcul côté client : écouter l'événement `input` du curseur, calculer la projection à partir des données KPIs déjà chargées, mettre à jour les valeurs affichées instantanément
- [x] 7.3 Assurer le responsive mobile (< 768px) : éléments empilés verticalement

## 8. Frontend — Section Deals Froids

- [x] 8.1 Ajouter un badge compteur "Deals Froids" dans la section KPIs existante (rouge si > 5, orange sinon, masqué si 0)
- [x] 8.2 Ajouter la section HTML "Deals Froids" dans `templates/dashboard.html` avec un tableau listant client, statut, montant, secteur, commercial, jours d'inactivité avec badges colorés (orange 10-20j, rouge > 20j) et message "Aucun deal froid" si liste vide
- [x] 8.3 Ajouter le JavaScript pour appeler `GET /api/analytics/cold-deals` et alimenter le badge compteur et le tableau
- [x] 8.4 Assurer le responsive mobile (< 768px) : tableau scrollable horizontalement

## 9. Intégration et tests visuels

- [x] 9.1 Vérifier que les 3 nouvelles sections s'intègrent visuellement avec le design existant (couleurs Tailwind, espacements, typographie cohérents)
- [x] 9.2 Tester le dashboard avec Playwright : vérifier le chargement des sections vitesse de vente, simulateur what-if et deals froids en desktop et mobile
- [x] 9.3 Vérifier la compatibilité SQLite/PostgreSQL des calculs de dates dans les nouvelles fonctions calculators.py
