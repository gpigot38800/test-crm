"""
Module API - Enregistrement des blueprints
"""


def register_blueprints(app):
    """
    Enregistre tous les blueprints API dans l'application Flask.

    Args:
        app: Instance Flask
    """
    from .deals import deals_bp
    from .analytics import analytics_bp
    from .upload import upload_bp
    from .sync import sync_bp

    app.register_blueprint(deals_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(sync_bp, url_prefix='/api')

    print("[OK] Blueprints API enregistres")
