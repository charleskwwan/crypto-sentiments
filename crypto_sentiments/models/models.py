# crypto_sentiments/models/models.py

from crypto_sentiments.models import db


class DateSentiment(db.Model):
    __tablename__ = 'date_sentiments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    sentiment = db.Column(db.String(15)) # allow null if no computable sentiment
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(),
                           onupdate=func.now())
