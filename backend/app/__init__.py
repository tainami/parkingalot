from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

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
        if db.engine.url.get_backend_name() == "sqlite":

            @event.listens_for(db.engine, "connect")
            def habilitar_fk_sqlite(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        db.create_all()

    return app
