# crypto_sentiments/views/visualizations.py

from flask import Blueprint
from flask import render_template
from crypto_sentiments.models.models import CurrencySentiment


visualizations = Blueprint(
    'visualizations',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@visualizations.route('/')
def index():
    csents = CurrencySentiment.query.all()
    for cs in csents:
        print(cs.currency, cs.date, cs.sentiment)
        
    return render_template('visualizations.html')
