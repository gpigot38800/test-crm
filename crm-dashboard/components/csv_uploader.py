"""
Composant Streamlit pour l'upload et le traitement de fichiers CSV.
Gère le parsing, la validation, les calculs et l'insertion en base de données.
"""

import streamlit as st
import pandas as pd
from typing import List
from business_logic.filters import normalize_column_names, map_csv_to_schema
from business_logic.validators import validate_csv_structure, validate_deal_row, ValidationError, parse_date
from business_logic.calculators import calculate_probability, calculate_weighted_value
from database.crud import insert_deals, clear_all_deals


def display_csv_uploader():
    """
    Affiche l'interface d'upload CSV dans la sidebar Streamlit.
    Gère tout le workflow: upload → parsing → validation → calculs → insertion.
    """
    st.sidebar.header("📥 Import de Données")

    # File uploader (n'accepte que les .csv)
    uploaded_file = st.sidebar.file_uploader(
        "Choisir un fichier CSV",
        type=['csv'],
        help="Fichier CSV contenant les colonnes: Client, Statut, Montant, Tags, Date Échéance, Assignee, Notes"
    )

    if uploaded_file is not None:
        # Bouton d'import
        if st.sidebar.button("🚀 Importer le CSV", type="primary"):
            _process_csv_upload(uploaded_file)


def _process_csv_upload(uploaded_file):
    """
    Traite le fichier CSV uploadé: parsing, validation, calculs, insertion.

    Args:
        uploaded_file: Fichier uploadé depuis Streamlit
    """
    # Container pour les messages de statut
    status_container = st.sidebar.container()

    with status_container:
        with st.spinner("Traitement en cours..."):
            try:
                # Étape 1: Parsing CSV avec gestion encodage
                df = _parse_csv_file(uploaded_file)

                # Étape 2: Normalisation des colonnes
                df = normalize_column_names(df)

                # Étape 3: Validation structure
                is_valid, missing_columns = validate_csv_structure(df)
                if not is_valid:
                    st.error(f"❌ Colonnes manquantes: {', '.join(missing_columns)}")
                    return

                # Étape 4: Mapping colonnes vers schéma DB
                df = map_csv_to_schema(df)

                # Étape 5: Validation business logic + calculs
                valid_deals, errors = _validate_and_calculate(df)

                # Étape 6: Affichage barre de progression (si >100 lignes)
                if len(valid_deals) > 100:
                    progress_bar = st.sidebar.progress(0)
                    progress_text = st.sidebar.empty()
                else:
                    progress_bar = None
                    progress_text = None

                # Étape 7: Clear database avant insertion
                clear_all_deals()

                # Étape 8: Insertion batch
                if valid_deals:
                    # Simulation progression (si barre active)
                    if progress_bar:
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            if i % 10 == 0:
                                progress_text.text(f"Insertion: {i+1}%")

                    inserted_count = insert_deals(valid_deals)

                    # Message succès
                    if len(errors) == 0:
                        st.success(f"✅ Import réussi: {inserted_count} deals importés")
                    else:
                        st.warning(f"⚠️ {inserted_count}/{len(df)} deals importés. {len(errors)} lignes rejetées.")

                    # Nettoyer progress bar
                    if progress_bar:
                        progress_bar.empty()
                        progress_text.empty()

                    # Forcer rechargement des données
                    if 'deals_df' in st.session_state:
                        del st.session_state['deals_df']

                else:
                    st.error("❌ Aucun deal valide à importer")

                # Étape 9: Afficher rapport d'erreurs si nécessaire
                if errors:
                    _display_error_report(errors)

            except Exception as e:
                st.error(f"❌ Erreur lors de l'import: {str(e)}")


def _parse_csv_file(uploaded_file) -> pd.DataFrame:
    """
    Parse le fichier CSV avec gestion des encodages UTF-8 et Latin-1.

    Args:
        uploaded_file: Fichier uploadé

    Returns:
        pd.DataFrame: DataFrame parsé

    Raises:
        Exception: Si le parsing échoue avec tous les encodages
    """
    try:
        # Tentative UTF-8 avec BOM
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        return df

    except UnicodeDecodeError:
        # Fallback Latin-1
        try:
            uploaded_file.seek(0)  # Reset file pointer
            df = pd.read_csv(uploaded_file, encoding='latin-1')
            st.sidebar.warning("⚠️ Fichier encodé en Latin-1 détecté")
            return df

        except Exception:
            raise Exception("Impossible de lire le fichier. Veuillez vérifier l'encodage (UTF-8 ou Latin-1 requis)")


def _validate_and_calculate(df: pd.DataFrame) -> tuple[List[dict], List[ValidationError]]:
    """
    Valide chaque ligne et calcule probabilité + valeur pondérée pour les lignes valides.

    Args:
        df: DataFrame avec colonnes mappées

    Returns:
        Tuple[List[dict], List[ValidationError]]: (deals valides, erreurs)
    """
    valid_deals = []
    all_errors = []

    for idx, row in df.iterrows():
        # Validation de la ligne
        errors = validate_deal_row(row, idx + 2)  # +2 car ligne 1 = headers

        if not errors:
            # Calcul probabilité
            probabilite = calculate_probability(row['statut'])

            # Calcul valeur pondérée
            valeur_ponderee = calculate_weighted_value(row['montant_brut'], probabilite)

            # Parser date si présente
            date_echeance = parse_date(str(row.get('date_echeance', ''))) if pd.notna(row.get('date_echeance')) else None

            # Créer dictionnaire deal
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
            all_errors.extend(errors)

    return valid_deals, all_errors


def _display_error_report(errors: List[ValidationError]):
    """
    Affiche un rapport détaillé des erreurs de validation.

    Args:
        errors: Liste des erreurs de validation
    """
    st.sidebar.error("⚠️ Erreurs de validation détectées")

    with st.sidebar.expander("Voir les détails des erreurs", expanded=False):
        # Créer un DataFrame pour affichage tabulaire
        error_data = []
        for error in errors:
            error_data.append({
                'Ligne': error.row_number,
                'Champ': error.field,
                'Erreur': error.message
            })

        error_df = pd.DataFrame(error_data)
        st.dataframe(error_df, width='stretch', hide_index=True)
