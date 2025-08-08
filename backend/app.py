# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from linkedin_auto_apply import run_apply

app = Flask(__name__)
CORS(app)  # autorise toutes les origines par défaut

@app.route('/')
def home():
    return 'Bienvenue sur la page d\'accueil de LinkedIn AutoApply!'

@app.route('/apply_jobs', methods=['POST', 'OPTIONS'])
def apply_jobs():
    # 1. Gérer le preflight CORS
    if request.method == 'OPTIONS':
        return ('', 204,
                {'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'POST, OPTIONS',
                 'Access-Control-Allow-Headers': 'Content-Type'})

    try:
        # 2. Récupération JSON
        data = request.get_json(force=True)

        # 3. Extraction des paramètres
        first_name        = data.get('firstName')
        last_name         = data.get('lastName')
        specialty         = data.get('specialty')
        experience_years  = data.get('experienceYears')
        linkedin_email    = data.get('email')
        linkedin_password = data.get('password')
        url_search        = data.get('urlSearch')

        # 4. Appel à votre fonction Selenium
        success, message = run_apply(
            first_name,
            last_name,
            specialty,
            experience_years,
            linkedin_email,
            linkedin_password,
            url_search
        )

        # 5. Renvoi JSON
        status = "success" if success else "error"
        return jsonify({"status": status, "message": message})

    except Exception as e:
        # 6. Log et renvoi JSON même en erreur
        app.logger.exception("Erreur dans /apply_jobs")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8081)
