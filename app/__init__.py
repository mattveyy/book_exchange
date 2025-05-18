"""
Инициализация Flask-приложения, регистрация blueprints, настройка базы данных.
"""
from flask import Flask
from app.extensions import db
from app.routes import books_bp, users_bp, exchange_bp
import os
from flask_cors import CORS


def create_app(config_override=None):
    app = Flask(__name__)

    if config_override:
        app.config.update(config_override)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'DATABASE_URL',
            'postgresql://postgres:postgres@localhost:5432/book_exchange'
        )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app, supports_credentials=True, expose_headers='*')

    app.register_blueprint(books_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(exchange_bp)

    db.init_app(app)
    return app
