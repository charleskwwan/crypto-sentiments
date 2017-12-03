# crypto_sentiments/models/__init__.py

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_db(app):
    """
    Creates all tables in the db and initializes it within the app
    """
    db.app = app
    db.init_app(app)
    db.create_all()
    return db


def drop_db():
    """
    Drops all tables in the db
    """
    db.session.remove()
    db.drop_all()
