# crypto_sentiments/__init__.py

from flask import Flask
from .views.home import home
from .views.predictions import predictions
from .views.visualizations import visualizations


app = Flask(__name__)


app.register_blueprint(home)
app.register_blueprint(predictions, url_prefix='/predict')
app.register_blueprint(visualizations, url_prefix='/viz')
