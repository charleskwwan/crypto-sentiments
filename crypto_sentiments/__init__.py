# crypto_sentiments/__init__.py

import datetime
import pickle
import threading

import schedule
from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from crypto_sentiments.common.sentiments.classify import TweetClassifier
from crypto_sentiments.common.sentiments.tracking import SentimentTracker
from crypto_sentiments.models import create_db
from crypto_sentiments.models import drop_db
from crypto_sentiments.views.home import home
from crypto_sentiments.views.predictions import predictions_factory
from crypto_sentiments.views.visualizations import visualizations


# _TRACK_SENTIMENT_FROM = datetime.datetime(2015, 1, 1)
_TRACK_SENTIMENT_FROM = datetime.datetime(2017, 12, 1)


app = Flask(__name__)


def initialize(conf, classifier_file):
    # config
    app.config.from_object(conf)

    # db creation
    create_db(app)

    # classifier
    print('### Loading classifier...')
    classifier = TweetClassifier.load(classifier_file)

    # routes
    app.register_blueprint(home)
    predictions = predictions_factory(classifier)
    app.register_blueprint(predictions, url_prefix='/predict')
    app.register_blueprint(visualizations, url_prefix='/viz')

    # track sentiment up to present
    sent_tracker = SentimentTracker(
        classifier,
        _TRACK_SENTIMENT_FROM,
    )
    print('### Tracking sentiments...')
    sent_tracker.track() # until today, updates db
    # schedule.every().day.at("1:00").do(sent_tracker.track) # update every day

    # optimizations
    CORS(app)
    Compress(app)


def shutdown():
    drop_db()
