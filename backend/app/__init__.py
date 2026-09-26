from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.routes import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)

    from app.cli import register_cli

    register_cli(app)

    with app.app_context():
        db.create_all()

    return app
