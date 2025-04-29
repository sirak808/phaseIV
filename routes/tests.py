from flask import Blueprint, render_template, request
from sqlalchemy import text
from extensions import db  # import db instance

tests_bp = Blueprint('tests', __name__, template_folder='tests')


@tests_bp.route('/test-db')
def test_db():
    try:
        db.session.execute(text('SELECT 1'))
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection failed: {e}'