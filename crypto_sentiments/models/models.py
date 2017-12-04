# crypto_sentiments/models/models.py

from crypto_sentiments.models import db
from sqlalchemy.sql import func


class CurrencySentiment(db.Model):
    __tablename__ = 'currency_sentiments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    sentiment = db.Column(db.Float, nullable=False) # +, 0, or -
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                           onupdate=func.now())


class CurrencyPrice(db.Model):
    __tablename__ = 'currency_prices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
