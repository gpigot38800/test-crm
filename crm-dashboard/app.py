"""
Dashboard CRM - Application Flask
Point d'entrée de l'application : gère l'initialisation Flask et l'enregistrement des routes.
"""

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template
from database.connection import init_database

# Créer l'application Flask
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['JSON_AS_ASCII'] = False  # Support caractères français dans JSON
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max pour upload CSV

# CORS pour développement local (optionnel)
# Si besoin d'appels API depuis autre origine: pip install flask-cors puis décommenter
# from flask_cors import CORS
# CORS(app)

# Initialiser la base de données au démarrage
with app.app_context():
    try:
        init_database()
        print("[OK] Base de donnees initialisee")
    except Exception as e:
        print(f"[ERREUR] Initialisation base de donnees: {str(e)}")

# Route principale
@app.route('/')
def index():
    """Affiche le dashboard principal"""
    return render_template('dashboard.html')

# Importer et enregistrer les blueprints API
from api import register_blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
