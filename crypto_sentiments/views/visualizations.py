# crypto_sentiments/views/visualizations.py

import random # temp

from crypto_sentiments.common.constants import CURRENCIES # temp
from crypto_sentiments.models.models import CurrencyPrice
from crypto_sentiments.models.models import CurrencySentiment
from flask import Blueprint
from flask import jsonify
from flask import render_template


visualizations = Blueprint(
    'visualizations',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@visualizations.route('/')
def index():
    # should be same length
    currency = random.choice(list(CURRENCIES.keys()))
    prices = {
        p.date: p.price
        for p in CurrencyPrice.query.filter_by(currency=currency)
    }
    sents = {
        s.date: s.sentiment
        for s in CurrencySentiment.query.filter_by(currency=currency)
    }
    pts = sorted([
        (date, prices[date], sents[date])
        for date in sents
    ], key=lambda t: t[0])

    start = random.randint(0, len(pts)-101)
    return render_template(
        'visualizations.html',
        pts=pts[start:start+100],
        currency=currency,
    )

@visualizations.route('/data', methods=['GET'])
def get_data(): 
    currency = random.choice(list(CURRENCIES.keys()))
    prices = {
        p.date: p.price
        for p in CurrencyPrice.query.filter_by(currency=currency)
    }
    sents = {
        s.date: s.sentiment
        for s in CurrencySentiment.query.filter_by(currency=currency)
    }
    pts = sorted([
        {'date': date.strftime('%Y-%m-%d'), 'price': prices[date], 'sentiment': sents[date]} 
        for date in sents  
    ], key=lambda t: t['date'])

    start = random.randint(0, len(pts)-101)

    return jsonify({'pts': pts[start:start+100], 'currency': currency})