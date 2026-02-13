# Deal Pulse

Application CRM pour fondateur avec objectif de maximiser le volume et la valeur des deals.

## Lancement

```bash
cd crm-dashboard
pip install -r requirements.txt
python app.py
```

Accès : http://localhost:5000/

## Endpoints API

| Methode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Page dashboard |
| GET | `/api/deals` | Liste tous les deals |
| DELETE | `/api/deals` | Supprime tous les deals |
| GET | `/api/kpis` | KPIs (pipeline, panier moyen, taux conversion) |
| GET | `/api/analytics/sectors` | Analyse par secteur (montants, paniers, Chart.js) |
| GET | `/api/analytics/deadlines` | Echeances depassees et a venir (30j) |
| POST | `/api/upload/csv` | Upload fichier CSV (multipart/form-data) |

## Format de reponse API

```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

## Stack technique

- **Backend** : Flask 3.0 + Python
- **Frontend** : HTML5 + Tailwind CSS (CDN) + Vanilla JS
- **Graphiques** : Chart.js 4.4.0
- **Base de donnees** : SQLite
- **Data** : pandas

## Documentation

- [PRD.md](../PRD.md) - Specifications fonctionnelles
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Architecture technique
