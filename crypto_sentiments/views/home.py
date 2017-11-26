# crypto_sentiments/views/home.py

from flask import Blueprint, render_template
from ..common.pricefinder import get_price
from ..common.tweet_scraper import scrape

from datetime import date

home = Blueprint(
    'home',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@home.route('/')
def index():


	scrape("#bitcoin", 100, "2017-10-01")

	# return str(get_price())
	return "Home"
