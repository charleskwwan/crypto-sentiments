# crypto_sentiments/views/predictions.py

import random # temp

from crypto_sentiments.common.constants import DIRECTIONS # temp
from crypto_sentiments.common.constants import SENTIMENTS # temp
from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request


predictions = Blueprint(
    'predictions',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@predictions.route('/', methods=['GET'])
def index():
    return render_template('predictions.html')


@predictions.route('/', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'tweet' not in data:
        return jsonify({'error': 'No tweet posted'}), 400

    response = {
        'sentiment': random.sample(SENTIMENTS, 1),
        'currencies': {
            'bitcoin': random.sample(DIRECTIONS, 1),
            'ethereum': random.sample(DIRECTIONS, 1),
            'litecoin': random.sample(DIRECTIONS, 1),
        },
    }
    return jsonify(response)
