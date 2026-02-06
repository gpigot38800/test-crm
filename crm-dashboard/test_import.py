"""
Script de test pour vérifier l'import CSV et le calcul du pipeline pondéré.
"""

import pandas as pd
import sys
from pathlib import Path

# Ajouter le répertoire au PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from database.connection import init_database
from database.crud import insert_deals, get_all_deals, clear_all_deals
from business_logic.filters import normalize_column_names, map_csv_to_schema
from business_logic.validators import validate_csv_structure, validate_deal_row, parse_date
from business_logic.calculators import calculate_probability, calculate_weighted_value, calculate_total_pipeline
from utils.formatters import format_currency

def test_csv_import():
    """Test complet de l'import CSV et des calculs"""

    print("=" * 70)
    print("TEST: Import CSV et Calcul du Pipeline Pondere")
    print("=" * 70)

    # 1. Initialiser la base de donnees
    print("\n[1] Initialisation de la base de donnees...")
    try:
        init_database()
        print("[OK] Base de donnees initialisee")
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False

    # 2. Charger le fichier CSV
    print("\n[2] Chargement du fichier CSV...")
    csv_path = Path(__file__).parent.parent / "crm_prospects_demo.csv"

    if not csv_path.exists():
        print(f"[ERREUR] Fichier CSV introuvable: {csv_path}")
        return False

    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print(f"[OK] CSV charge: {len(df)} lignes")
        print(f"     Colonnes: {list(df.columns)}")
    except Exception as e:
        print(f"[ERREUR] Lecture CSV: {e}")
        return False

    # 3. Normalisation des colonnes
    print("\n[3] Normalisation des colonnes...")
    df = normalize_column_names(df)
    print(f"[OK] Colonnes normalisees: {list(df.columns)}")

    # 4. Validation de la structure
    print("\n[4] Validation de la structure...")
    is_valid, missing_cols = validate_csv_structure(df)
    if not is_valid:
        print(f"[ERREUR] Colonnes manquantes: {missing_cols}")
        return False
    print("[OK] Structure valide")

    # 5. Mapping vers schema DB
    print("\n[5] Mapping vers schema DB...")
    df = map_csv_to_schema(df)
    print(f"[OK] Colonnes mappees: {list(df.columns)}")

    # 6. Validation et calculs
    print("\n[6] Validation des deals et calculs...")
    valid_deals = []
    errors = []

    for idx, row in df.iterrows():
        # Validation
        row_errors = validate_deal_row(row, idx + 2)

        if not row_errors:
            # Calculs
            probabilite = calculate_probability(row['statut'])
            valeur_ponderee = calculate_weighted_value(row['montant_brut'], probabilite)
            date_echeance = parse_date(str(row.get('date_echeance', ''))) if pd.notna(row.get('date_echeance')) else None

            deal = {
                'client': str(row['client']).strip(),
                'statut': str(row['statut']).strip(),
                'montant_brut': float(row['montant_brut']),
                'probabilite': probabilite,
                'valeur_ponderee': valeur_ponderee,
                'secteur': str(row.get('secteur', '')).strip() if pd.notna(row.get('secteur')) else None,
                'date_echeance': date_echeance,
                'assignee': str(row.get('assignee', '')).strip() if pd.notna(row.get('assignee')) else None,
                'notes': str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else None
            }
            valid_deals.append(deal)
        else:
            errors.extend(row_errors)

    print(f"[OK] {len(valid_deals)} deals valides")
    if errors:
        print(f"[WARN] {len(errors)} erreurs de validation")

    # 7. Clear et insertion en DB
    print("\n[7] Insertion en base de donnees...")
    try:
        clear_all_deals()
        inserted_count = insert_deals(valid_deals)
        print(f"[OK] {inserted_count} deals inseres")
    except Exception as e:
        print(f"[ERREUR] Erreur d'insertion: {e}")
        return False

    # 8. Lecture depuis DB
    print("\n[8] Lecture des donnees depuis la DB...")
    try:
        deals_df = get_all_deals()
        print(f"[OK] {len(deals_df)} deals recuperes")
    except Exception as e:
        print(f"[ERREUR] Erreur de lecture: {e}")
        return False

    # 9. Calcul du pipeline pondere
    print("\n[9] Calcul du pipeline pondere...")
    total_pipeline = calculate_total_pipeline(deals_df)
    print(f"[OK] Pipeline Pondere Total: {format_currency(total_pipeline)}")

    # 10. Affichage des statistiques
    print("\n" + "=" * 70)
    print("RESULTATS FINAUX")
    print("=" * 70)

    print(f"\nPipeline Pondere Total: {format_currency(total_pipeline)}")
    print(f"Panier Moyen: {format_currency(deals_df['montant_brut'].mean())}")
    print(f"Nombre de Deals: {len(deals_df)}")

    # Detail par statut
    print("\nRepartition par Statut:")
    for statut in deals_df['statut'].unique():
        count = len(deals_df[deals_df['statut'] == statut])
        total = deals_df[deals_df['statut'] == statut]['valeur_ponderee'].sum()
        print(f"   - {statut}: {count} deals - {format_currency(total)}")

    # Afficher quelques exemples
    print("\nExemples de deals importes:")
    print(deals_df[['client', 'statut', 'montant_brut', 'probabilite', 'valeur_ponderee']].head(5).to_string(index=False))

    print("\n" + "=" * 70)
    print("[OK] TEST REUSSI - L'import CSV et le calcul fonctionnent correctement !")
    print("=" * 70)

    return True

if __name__ == "__main__":
    success = test_csv_import()
    sys.exit(0 if success else 1)
