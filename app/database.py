from flask import g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def get_db(e=None):
    if "db" not in g:
        g.db = db


def close_db(e=None):
    global db
    db.session.remove()
    g.pop("db", None)


def init_app(app):
    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        app.before_request(get_db)
        app.teardown_appcontext(close_db)
        # app.cli.add_command(create_db_command)
