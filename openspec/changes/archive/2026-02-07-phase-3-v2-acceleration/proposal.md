## Why

Le dashboard CRM a complété les Phases 1 (MVP) et 2 (V1) avec succès : import CSV, KPIs, analyse sectorielle, CRUD deals, filtres avancés et performance commerciale sont opérationnels. Cependant, le fondateur manque d'outils d'accélération commerciale : il ne peut pas mesurer la rapidité de conversion des deals, ni simuler l'impact de stratégies tarifaires, ni identifier les deals qui stagnent et nécessitent une relance. La Phase 3 (V2) apporte ces capacités décisionnelles pour passer du pilotage passif à l'action proactive.

## What Changes

- Ajout d'une section **Vitesse de Vente** affichant le temps moyen pour convertir un deal de "Prospect" à "Gagné", basé sur les champs `created_at` et `updated_at` existants
- Ajout d'un **Simulateur "What-If"** avec un curseur interactif permettant de projeter l'impact sur le pipeline pondéré d'une variation du panier moyen (ex: +10%, +20%)
- Ajout d'un système de **Relances automatiques** avec marquage visuel des deals "froids" (aucune mise à jour depuis 10 jours) et indicateurs dans le dashboard
- Ajout de nouveaux endpoints API Flask pour alimenter ces fonctionnalités
- Extension du dashboard HTML/JS existant avec de nouvelles sections et composants Chart.js

## Capabilities

### New Capabilities
- `sales-velocity`: Calcul et affichage du temps moyen de conversion des deals par statut, avec métriques de vitesse de vente (jours moyens Prospect → Gagné, par secteur, par commercial)
- `what-if-simulator`: Simulateur interactif avec curseur permettant de projeter l'impact d'une variation du panier moyen sur le pipeline pondéré total et par statut
- `cold-deals-tracker`: Détection et marquage visuel des deals "froids" (pas de mise à jour depuis 10+ jours), avec liste dédiée et indicateurs d'alerte dans le dashboard

### Modified Capabilities
- `kpi-calculator`: Ajout de nouveaux KPIs (vitesse de vente moyenne, nombre de deals froids) dans la section métriques flash existante

## Impact

- **Backend** : Nouveaux endpoints dans `api/analytics.py`, nouvelles fonctions dans `business_logic/calculators.py`
- **Frontend** : Nouvelles sections dans `dashboard.html`, nouveau JavaScript pour le slider what-if et le marquage visuel des deals froids
- **Base de données** : Aucune modification de schéma nécessaire — les champs `created_at` et `updated_at` existants suffisent pour la vélocité et la détection des deals froids
- **Dépendances** : Aucune nouvelle bibliothèque requise — Chart.js et le stack Flask existant couvrent les besoins
- **Limitation connue** : La vitesse de vente se base sur `created_at` → `updated_at` des deals "Gagné", sans historique intermédiaire des transitions de statut (acceptable pour le MVP V2)
