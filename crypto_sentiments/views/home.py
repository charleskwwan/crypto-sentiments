# crypto_sentiments/views/home.py

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
_price_directions = {
    'bitcoin': 'up',
    'ethereum': 'down',
    'litecoin': 'up',
}


@home.route('/')
def index():
    return render_template(
        'index.html',
        currency=_DEFAULT_CURRENCY,
        direction=_price_directions[_DEFAULT_CURRENCY],
        currencies=[c for c in _price_directions.keys()],
    )


@home.route('/pricedir/<string:currency>', methods=['GET'])
def pricedir(currency):
    if currency in _price_directions:
        return jsonify({'direction': _price_directions[currency]})
    else:
        return jsonify({'error': 'Invalid currency'})
