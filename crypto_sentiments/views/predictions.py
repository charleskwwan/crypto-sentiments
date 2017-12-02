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
    """
    API to allow clients to post tweets for analysis
    
    Parameters:
    - tweet [str]: tweet string

    Returns (in JSON):
    - sentiment [str]: the overall sentiment of the tweet
        - positive, negative, or neutral
    - currencies [dict]: any currencies more specifically we can predict price
        changes for, optional
        - for ex, if a tweet predicts increases in bitcoin, but decreases in
          litecoin, then currencies = {
              'bitcoin': 'up',
              'litecoin': 'down',
          }
    """
    data = request.get_json()
    if not data or 'tweet' not in data:
        return jsonify({'error': 'No tweet posted'}), 400

    response = {
        'sentiment': random.sample(SENTIMENTS, 1)[0],
        'currencies': {
            'bitcoin': random.sample(DIRECTIONS, 1)[0],
            'ethereum': random.sample(DIRECTIONS, 1)[0],
            'litecoin': random.sample(DIRECTIONS, 1)[0],
        },
    }
    return jsonify(response)
