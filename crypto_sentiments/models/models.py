# crypto_sentiments/models/models.py

import datetime

import jsonpickle
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

    def serialize(self):
        return {
            'currency': self.currency,
            'date': self.date.strftime('%Y-%m-%d'),
            'sentiment': str(self.sentiment),
        }

    @classmethod
    def deserialize(cls, serialized):
        return cls(
            currency=serialized['currency'],
            date=datetime.datetime.strptime(serialized['date'], '%Y-%m-%d'),
            sentiment=float(erialized['sentiment']),
        )


class CurrencyPrice(db.Model):
    __tablename__ = 'currency_prices'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    currency = db.Column(db.String(20), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    price = db.Column(db.Float, nullable=True) # no price data available then
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def serialize(self):
        return {
            'currency': self.currency,
            'date': self.date.strftime('%Y-%m-%d'),
            'price': str(self.price),
        }

    @classmethod
    def deserialize(cls, serialized):
        return cls(
            currency=serialized['currency'],
            date=datetime.datetime.strptime(serialized['date'], '%Y-%m-%d'),
            price=float(serialized['price']),
        )


_MODELS = {
    'CurrencySentiment': CurrencySentiment,
    'CurrencyPrice': CurrencyPrice
}


def save_tables(fname):
    """
    Saves all tables to a json file

    Params:
    - fname [str]: file name
    """
    frozen = jsonpickle.encode({
        k : [entry.serialize() for entry in v.query.all()]
        for k, v in _MODELS
    })
    with open(fname, 'w+') as f:
        f.write(frozen)


def load_tables(fname):
    with open(fname, 'r') as f:
        raw = f.read()
    for k, v in jsonpickle.decode(raw):
        clss = _MODELS[k]
        for serialized in v:
            entry = clss.deserialize(serialized)
            db.session.add(entry)
    db.session.commit()
