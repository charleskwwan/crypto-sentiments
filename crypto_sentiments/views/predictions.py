# crypto_sentiments/views/predictions.py

from flask import Blueprint, render_template


predictions = Blueprint(
    'predictions',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@predictions.route('/')
def index():
    return render_template('predictions.html')
