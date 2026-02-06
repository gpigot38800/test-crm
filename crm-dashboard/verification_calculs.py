"""
Verification manuelle des calculs du pipeline pondere
Compare les donnees CSV avec les resultats de l'application
"""

import pandas as pd
from pathlib import Path

# Charger le CSV
csv_path = Path(__file__).parent.parent / "crm_prospects_demo.csv"
df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("=" * 80)
print("VERIFICATION MANUELLE DES CALCULS DU PIPELINE PONDERE")
print("=" * 80)

# Mapping des probabilites
prob_map = {
    'prospect': 0.10,
    'qualifie': 0.30,
    'qualifi\u00e9': 0.30,  # Avec accent
    'negociation': 0.70,
    'n\u00e9gociation': 0.70,  # Avec accent
    'gagne': 1.00,
    'gagn\u00e9': 1.00,  # Avec accent
    'gagne - en cours': 1.00,
    'gagn\u00e9 - en cours': 1.00  # Avec accent
}

# Normaliser les statuts
df['Status_normalized'] = df['Status'].str.lower().str.strip()

# Calculer les valeurs ponderees
results_by_status = {}
total_pipeline = 0
valid_count = 0
rejected_count = 0
rejected_deals = []

print("\nANALYSE PAR DEAL:")
print("-" * 80)

for idx, row in df.iterrows():
    client = row['Task Name']
    statut = row['Status']
    statut_norm = row['Status_normalized']
    montant = float(row['Montant Deal'])

    if statut_norm in prob_map:
        prob = prob_map[statut_norm]
        valeur_ponderee = montant * prob

        # Ajouter au total
        total_pipeline += valeur_ponderee
        valid_count += 1

        # Grouper par statut
        if statut not in results_by_status:
            results_by_status[statut] = {'count': 0, 'montant_total': 0, 'valeur_ponderee_total': 0, 'deals': []}

        results_by_status[statut]['count'] += 1
        results_by_status[statut]['montant_total'] += montant
        results_by_status[statut]['valeur_ponderee_total'] += valeur_ponderee
        results_by_status[statut]['deals'].append({
            'client': client,
            'montant': montant,
            'prob': prob,
            'valeur_ponderee': valeur_ponderee
        })

        print(f"[OK] {client:40s} | {statut:20s} | {montant:>10,.0f} EUR x {prob:>4.0%} = {valeur_ponderee:>10,.2f} EUR")
    else:
        rejected_count += 1
        rejected_deals.append({
            'client': client,
            'statut': statut,
            'montant': montant
        })
        print(f"[REJETE] {client:40s} | {statut:20s} | {montant:>10,.0f} EUR (statut non reconnu)")

print("\n" + "=" * 80)
print("RESULTATS PAR STATUT:")
print("=" * 80)

for statut, data in sorted(results_by_status.items()):
    print(f"\n{statut.upper()}")
    print(f"  Nombre de deals: {data['count']}")
    print(f"  Montant total brut: {data['montant_total']:,.2f} EUR")
    print(f"  Valeur ponderee totale: {data['valeur_ponderee_total']:,.2f} EUR")
    print(f"  Details:")
    for deal in data['deals']:
        print(f"    - {deal['client']:40s} | {deal['montant']:>10,.0f} x {deal['prob']:>4.0%} = {deal['valeur_ponderee']:>10,.2f}")

if rejected_deals:
    print("\n" + "=" * 80)
    print("DEALS REJETES (Statut non reconnu):")
    print("=" * 80)
    for deal in rejected_deals:
        print(f"  - {deal['client']:40s} | {deal['statut']:20s} | {deal['montant']:>10,.0f} EUR")

print("\n" + "=" * 80)
print("SYNTHESE FINALE:")
print("=" * 80)

print(f"\nDeals traites: {valid_count}")
print(f"Deals rejetes: {rejected_count}")
print(f"Total deals: {len(df)}")

print(f"\nPIPELINE PONDERE TOTAL: {total_pipeline:,.2f} EUR")

# Calculer le panier moyen
montants_valides = [row['Montant Deal'] for _, row in df.iterrows()
                    if row['Status_normalized'] in prob_map]
panier_moyen = sum(montants_valides) / len(montants_valides) if montants_valides else 0

print(f"PANIER MOYEN: {panier_moyen:,.2f} EUR")
print(f"MONTANT TOTAL BRUT: {sum(montants_valides):,.2f} EUR")

print("\n" + "=" * 80)
print("VERIFICATION:")
print("=" * 80)

print("\nResultats attendus (de l'application):")
print("  Pipeline Pondere Total: 162 430,00 EUR")
print("  Panier Moyen: 14 100,00 EUR")
print("  Nombre de Deals: 22")

print("\nResultats calcules:")
print(f"  Pipeline Pondere Total: {total_pipeline:,.2f} EUR")
print(f"  Panier Moyen: {panier_moyen:,.2f} EUR")
print(f"  Nombre de Deals: {valid_count}")

# Verification
if abs(total_pipeline - 162430) < 0.01 and abs(panier_moyen - 14100) < 0.01 and valid_count == 22:
    print("\n[OK] TOUS LES CALCULS SONT CORRECTS !")
else:
    print("\n[ERREUR] Les calculs ne correspondent pas !")

print("=" * 80)
