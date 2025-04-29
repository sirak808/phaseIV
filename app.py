# filename: app.py
from flask import Flask, render_template, request, redirect, flash, url_for 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from extensions import db
import os
# Make sure to import load_dotenv 
from dotenv import load_dotenv 

# --- Import Blueprints ---
from routes.tests import tests_bp
from routes.views import views_bp
from routes.procedures import procedures_bp
# ------------------------

def create_app():
    # Load .env file - place this early
    load_dotenv() 

    app = Flask(__name__)

    # Configure the SQLAlchemy part
    db_uri = os.getenv('DATABASE_URI')
    if db_uri is None:
        # This check is useful - stop if URI is missing
        raise ValueError("FATAL ERROR: DATABASE_URI environment variable not found. Check .env file.") 

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Load secret key, provide a default for safety if not found
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_very_default_secret_key_123') 

    db.init_app(app)

    # --- Define Routes ---
    @app.route('/')
    def home():
        return render_template('home.html')

    # --- Register Blueprints ---
    app.register_blueprint(tests_bp)
    app.register_blueprint(views_bp)
    app.register_blueprint(procedures_bp)
    # -------------------------

    return app

# --- Main execution ---
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)