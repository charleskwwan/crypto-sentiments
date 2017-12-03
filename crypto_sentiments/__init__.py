# crypto_sentiments/__init__.py

from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from crypto_sentiments.models import create_db
from crypto_sentiments.views.home import home
from crypto_sentiments.views.predictions import predictions
from crypto_sentiments.views.visualizations import visualizations


def run(conf):
    app = Flask(__name__)
    app.config.from_object(conf)

    app.register_blueprint(home)
    app.register_blueprint(predictions, url_prefix='/predict')
    app.register_blueprint(visualizations, url_prefix='/viz')

    # db creation
    create_db(app)

    # optimizations
    CORS(app)
    Compress(app)

    app.run()
