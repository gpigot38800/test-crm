Voici le document final complet, structuré et prêt à être utilisé. Ce format Markdown est conçu pour être 
# 🚀 Spécifications : Dashboard CRM Fondateur (Focus Valeur & Volume)

## 1. Vision du Projet

* **Utilisateur cible :** Fondateur de l'entreprise (usage personnel).
* **Objectif Business :** Maximiser le volume de deals et leur valeur unitaire.
* **Philosophie :** Pas de fioritures techniques, uniquement des indicateurs décisionnels.

---

## 3. Architecture de la Base de Données (SQLite)

L'agent doit créer une table `deals` avec les colonnes suivantes :

| Champ | Type | Description / Règle métier |
| --- | --- | --- |
| `id` | Integer | Clé primaire. |
| `client` | String | Nom du prospect ou de l'entreprise. |
| `statut` | String | Prospect, Qualifié, Négociation, Gagné. |
| `montant_brut` | Float | Valeur totale du deal. |
| `probabilite` | Float | **Automatique** : 10% (Prospect), 30% (Qualifié), 70% (Négo), 100% (Gagné). |
| `valeur_ponderee` | Float | **Calculé** : `montant_brut` * `probabilite`. |
| `secteur` | String | Tags extraits (ex: Tech, Sport, Énergie). |
| `date_echeance` | Date | Date de clôture prévue (`Due Date`). |
| `assignee` | String | Commercial responsable. |
| `notes` | Text | Détails additionnels sur le deal. |

---

## 4. Roadmap de Développement

### 🟢 PHASE 1 : MVP (Indispensable immédiatement)

* **Import CSV :** Module capable de lire le fichier `crm_prospects_demo.csv` et de peupler la base SQLite.
* **Calculateur de Pipe Pondéré :** Somme globale de la valeur pondérée pour prévoir le CA réel.
* **Analyse par Secteur (Maximisation Valeur) :** * Graphique en barres montrant le montant total par secteur (Tags).
* Objectif : Identifier les secteurs à haut panier moyen.


* **Gestion des Échéances (Maximisation Volume) :**
* Liste rouge des deals dont la date d'échéance est dépassée.
* Vue des signatures attendues sur les 30 prochains jours.


* **KPIs Flash :** Panier moyen actuel, montant total du pipe, et taux de conversion global.

### 🔵 PHASE 2 : V1 (Pilotage & Saisie)

* **Saisie Manuelle :** Formulaire pour ajouter ou modifier un deal sans ré-importer le CSV.
* **Performance Commerciale :** Analyse du volume de deals gérés par chaque commercial et leur taux de succès.
* **Filtres Avancés :** Filtrer le dashboard par secteur, priorité ou commercial.

### 🟣 PHASE 3 : V2 (Accélération)

* **Vitesse de Vente :** Temps moyen pour passer de "Prospect" à "Gagné".
* **Simulateur "What-If" :** Curseur permettant de simuler l'impact sur le CA d'une hausse de 10% du panier moyen.
* **Relances automatiques :** Marquage visuel des deals "froids" (pas de mise à jour depuis 10 jours).

---

## 5. ⏳ Section "+ TARD" (Hors-périmètre actuel)

*Ces points sont exclus du développement actuel pour garantir la rapidité de livraison :*

* **Sécurité :** Pas de login, pas de gestion de mots de passe.
* **Multi-accès :** Pas de comptes collaborateurs.
* **Connecteurs API :** Pas de lien direct (type Zapier/Hubspot), on reste sur l'import CSV.
* **Paiement :** Pas de facturation intégrée.

---

## 6. Prompt pour votre Agent de Codage

> *"Agis comme un développeur Python expert en Data. Je veux créer l'application décrite dans ce document. Utilise **Streamlit** et **SQLite**.
> Étape 1 : Crée le script d'initialisation de la base de données.
> Étape 2 : Crée l'interface d'upload pour mon fichier CSV et assure-toi que les probabilités (10%, 30%, 70%, 100%) sont appliquées automatiquement selon le statut.
> Étape 3 : Affiche le dashboard MVP avec le pipeline pondéré, l'analyse par secteur et les alertes sur les dates dépassées."*