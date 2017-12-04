"""
crypto_sentiments/common/pricefinder.py
https://github.com/lagerfeuer/cryptocompare
Notes:
- API calls to cryptocompare take awhile, should be used sparingly and
  and cache results if possible
"""

from datetime import datetime as dt
from datetime import timedelta
from concurrent.futures import ThreadPoolExecutor

import cryptocompare as cc
from crypto_sentiments.common.dateutils import daterange


COINS = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'litecoin': 'LTC',
}
_CURRENCIES = set(['USD'])


def get_price(coin='BTC', currency='USD', date=None):
    """
    Get price of cryptocurrency in terms of real currency on a specific day

    Params:
    coin [str]: cryptocurrency code
    currency [str]: real currency code
    date [datetime]: year, month, day of price

    Return [float]: price of coin in currency

    Example:
    get_price('BTC', 'USD', datetime.datetime(2017, 10, 26))
    """
    if date:
        dct = cc.get_historical_price(coin, currency, date)
    else:
        dct = cc.get_price(coin, currency, full=False)
    return dct[coin][currency] if dct else None


def get_price_in_range(coin, currency, start, end):
    """
    Gets the price of cryptocurrency in terms of real currency over a range of
    dates, exclusive.

    Params:
    coin [str]: cryptocurrency code
    currency [str]: real currency code
    start [datetime]: starting year, month, day
    end [datetime]: end year, month, day

    Return [list[(float, datetime)]]: prices of coin in currency, in day order

    Example:
    get_price_in_range(
        'BTC',
        'USD',
        datetime.datetime(2016, 6, 15),
        datetime.datetime(2017, 4, 12),
    )
    """
    prices = []
    pool = ThreadPoolExecutor(max_workers=5)

    def record_price(dt):
        price = get_price(coin, currency, dt) # can be 0, if coin didnt exist
        prices.append((price, dt))

    for dt in daterange(start, end):
        pool.submit(record_price, dt)
    pool.shutdown()

    return prices
