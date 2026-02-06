"""
Module API - Enregistrement des blueprints
"""

def register_blueprints(app):
    """
    Enregistre tous les blueprints API dans l'application Flask.

    Args:
        app: Instance Flask
    """
    # Import des blueprints (sera ajouté au fur et à mesure)
    # from .deals import deals_bp
    # from .analytics import analytics_bp
    # from .upload import upload_bp

    # Enregistrement des blueprints
    # app.register_blueprint(deals_bp, url_prefix='/api')
    # app.register_blueprint(analytics_bp, url_prefix='/api')
    # app.register_blueprint(upload_bp, url_prefix='/api')

    print("[OK] Blueprints API enregistres")
