"""
Fonctions utilitaires de formatage.
Fournit les fonctions de formatage pour l'affichage des montants, dates, etc.
"""


def format_currency(amount: float) -> str:
    """
    Formate un montant en euros avec séparateurs de milliers.

    Args:
        amount: Montant à formater

    Returns:
        str: Montant formaté (ex: "1 500 000 €")

    Examples:
        >>> format_currency(1500000)
        '1 500 000 €'
        >>> format_currency(15000.50)
        '15 000,50 €'
    """
    # Formater avec séparateur d'espace pour les milliers et virgule pour les décimales
    formatted = f"{amount:,.2f}".replace(",", " ").replace(".", ",")

    # Supprimer les décimales si elles sont à zéro
    if formatted.endswith(",00"):
        formatted = formatted[:-3]

    return f"{formatted} €"
