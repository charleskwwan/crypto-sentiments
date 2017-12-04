# crypto_sentiments/views/visualizations.py

from flask import Blueprint
from flask import render_template


visualizations = Blueprint(
    'visualizations',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@visualizations.route('/')
def index():
    return render_template('visualizations.html')
