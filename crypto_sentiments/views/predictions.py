# crypto_sentiments/views/predictions.py

import random # temp

from crypto_sentiments.common.constants import DIRECTIONS # temp
from crypto_sentiments.common.constants import SENTIMENTS # temp
from crypto_sentiments.common.sentiments.twitter_scrape import prune_tweet
from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request


def predictions_factory(
    classifier,
    pos='positive',
    neg='negative',
    neu='neutral',
):
    """
    Factory to create predictions routes blueprint since classifier is required
    from toplevel

    Params:
    - classifier [obj]: tweet classifier, must have .classifiy function
    - pos_tag [str]: positive 
    """

    predictions = Blueprint(
        'predictions',
        __name__,
        template_folder='templates',
        static_folder='static',
    )
    sents = {
        pos: 'positive',
        neg: 'negative',
        neu: 'neutral',
    }

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

        Notes:
        - Example response:
                response = {
                    'sentiment': random.sample(SENTIMENTS, 1)[0],
                    'currencies': {
                        'bitcoin': random.sample(DIRECTIONS, 1)[0],
                        'ethereum': random.sample(DIRECTIONS, 1)[0],
                        'litecoin': random.sample(DIRECTIONS, 1)[0],
                    },
                }
        """
        data = request.get_json()
        if not data or 'tweet' not in data:
            return jsonify({'error': 'No tweet posted'}), 400

        tweet = prune_tweet(data['tweet'])
        sent = classifier.classify(tweet)
        response = {
            'sentiment': sents[sent]
        }

        return jsonify(response)

    return predictions
