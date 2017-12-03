# crypto_sentiments/views/home.py

import random # temp

from crypto_sentiments.common.constants import CURRENCIES
from crypto_sentiments.common.constants import DIRECTIONS # temp
from crypto_sentiments.common.constants import SENTIMENTS # temp
from crypto_sentiments.common.pricefinder import get_price
from flask import Blueprint
from flask import jsonify
from flask import render_template


home = Blueprint(
    'home',
    __name__,
    template_folder='templates',
    static_folder='static',
)

_DEFAULT_CURRENCY = 'bitcoin'


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
        direction=random.sample(DIRECTIONS, 1)[0],
        currencies=[c for c in CURRENCIES],
    )


@home.route('/pricedir/<string:currency>', methods=['GET'])
def pricedir(currency):
    """
    API to allow clients to query the price direction for a specific currency
    """
    if currency in CURRENCIES:
        return jsonify({'direction': random.sample(DIRECTIONS, 1)[0]})
    else:
        return jsonify({'error': 'Invalid currency'}), 400
