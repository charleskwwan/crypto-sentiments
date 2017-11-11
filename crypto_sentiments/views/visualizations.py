# crypto_sentiments/views/visualizations.py

from flask import Blueprint, render_template


visualizations = Blueprint(
    'visualizations',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@visualizations.route('/')
def index():
    return "Visualizations" 
