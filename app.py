from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from extensions import db
import os
from dotenv import load_dotenv

def create_app():

    app = Flask(__name__)

    # Configure the SQLAlchemy part
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    from routes.tests import tests_bp
    from routes.views import views_bp
    app.register_blueprint(tests_bp)
    app.register_blueprint(views_bp)

    return app




if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
