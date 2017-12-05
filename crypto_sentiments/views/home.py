# crypto_sentiments/views/home.py

import random # temp

from crypto_sentiments.common.constants import CURRENCIES
from crypto_sentiments.common.dateutils import today
from crypto_sentiments.common.trends import feature_on
from flask import Blueprint
from flask import jsonify
from flask import render_template


_DEFAULT_CURRENCY = 'bitcoin'


def _get_direction(currency, predictors):
    predictor = predictors[currency]
    feature = feature_on(today(), currency)
    return predictor.predict(feature)


def home_factory(predictors):
    home = Blueprint(
        'home',
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    @home.route('/', methods=['GET'])
    def index():
        """
        Renders home page with following Jinja2 vars:
        - currency: default currency on page
        - direction: price direction of currency
        - currencies: every supported currency (so html can render buttons for each)
        """
        return render_template(
            'index.html',
            currency=_DEFAULT_CURRENCY,
            direction=_get_direction(_DEFAULT_CURRENCY, predictors),
            currencies=[c for c in CURRENCIES],
        )

    @home.route('/pricedir/<string:currency>', methods=['GET'])
    def pricedir(currency):
        """
        API to allow clients to query the price direction for a specific currency
        """
        if currency in CURRENCIES:
            direction = _get_direction(currency, predictors)
            return jsonify({'direction': direction})
        else:
            return jsonify({'error': 'Invalid currency'}), 400

    return home
