"""
Blueprint API pour l'upload CSV.
Expose l'endpoint POST /api/upload/csv.
"""

import io
import pandas as pd
from flask import Blueprint, jsonify, request
from database.crud import clear_all_deals, insert_deals
from business_logic.filters import normalize_column_names, map_csv_to_schema
from business_logic.validators import validate_csv_structure, validate_deal_row
from business_logic.calculators import calculate_probability, calculate_weighted_value

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload/csv', methods=['POST'])
def upload_csv():
    """POST /api/upload/csv - Upload et traitement d'un fichier CSV"""
    try:
        # Vérifier la présence du fichier
        if 'file' not in request.files:
            return jsonify({"success": False, "data": None, "error": "Aucun fichier fourni"}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({"success": False, "data": None, "error": "Aucun fichier sélectionné"}), 400

        # Valider type fichier
        if not file.filename.lower().endswith('.csv'):
            return jsonify({"success": False, "data": None, "error": "Seuls les fichiers .csv sont acceptés"}), 400

        # Lire le CSV depuis le stream mémoire
        try:
            content = file.read()
            try:
                df = pd.read_csv(io.BytesIO(content), encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding='latin-1')
        except Exception as e:
            return jsonify({"success": False, "data": None, "error": f"Erreur de lecture CSV: {str(e)}"}), 400

        # Normaliser les colonnes
        df = normalize_column_names(df)

        # Valider la structure
        is_valid, missing_cols = validate_csv_structure(df)
        if not is_valid:
            return jsonify({"success": False, "data": None,
                            "error": f"Colonnes manquantes: {', '.join(missing_cols)}"}), 400

        # Mapper les colonnes CSV vers le schéma DB
        df = map_csv_to_schema(df)

        # Traiter chaque ligne
        deals_to_insert = []
        errors = []

        for idx, row in df.iterrows():
            row_errors = validate_deal_row(row, idx + 1)
            if row_errors:
                errors.extend([str(e) for e in row_errors])
                continue

            # Calculer probabilité et valeur pondérée
            statut = str(row.get('statut', '')).strip()
            montant_brut = float(row.get('montant_brut', 0))
            probabilite = calculate_probability(statut)
            valeur_ponderee = calculate_weighted_value(montant_brut, probabilite)

            deal = {
                'client': str(row.get('client', '')).strip(),
                'statut': statut,
                'montant_brut': montant_brut,
                'probabilite': probabilite,
                'valeur_ponderee': valeur_ponderee,
                'secteur': str(row.get('secteur', '')).strip() if pd.notna(row.get('secteur')) else None,
                'date_echeance': str(row.get('date_echeance', '')).strip() if pd.notna(row.get('date_echeance')) else None,
                'assignee': str(row.get('assignee', '')).strip() if pd.notna(row.get('assignee')) else None,
                'notes': str(row.get('notes', '')).strip() if pd.notna(row.get('notes')) else None
            }
            deals_to_insert.append(deal)

        if not deals_to_insert:
            return jsonify({"success": False, "data": None,
                            "error": "Aucun deal valide trouvé dans le fichier"}), 400

        # Clear et insert
        clear_all_deals()
        nb_inserted = insert_deals(deals_to_insert)

        return jsonify({"success": True, "data": {
            "nb_imported": nb_inserted,
            "nb_errors": len(errors),
            "errors": errors[:10] if errors else []
        }, "error": None})

    except Exception as e:
        return jsonify({"success": False, "data": None, "error": str(e)}), 500
