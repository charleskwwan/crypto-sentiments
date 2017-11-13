"""
crypto_sentiments/common/pricefinder.py
https://github.com/lagerfeuer/cryptocompare
Notes:
- API calls to cryptocompare take awhile, should be used sparingly and
  and cache results if possible
"""

import cryptocompare as cc

from datetime import datetime as dt
from datetime import timedelta


COINS = set(['BTC', 'ETH', 'LTC'])
CURRENCIES = set(['USD'])


def get_price(coin, currency, date=None):
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


def _daterange(start, end):
    """
    Generator for dates between start and end inclusive
    """
    for n in range(int((end - start).days)+1):
        yield start + timedelta(n)


def get_price_in_range(coin, currency, start, end):
    """
    Gets the price of cryptocurrency in terms of real currency over a range of
    dates, inclusive.

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
    for dt in _daterange(start, end):
        price = get_price(coin, currency, dt)
        if price:
            prices.append((price, dt))
        else:
            return None
    return prices
