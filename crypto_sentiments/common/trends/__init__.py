# crypto_sentiments/common/trends/__init__.py

import datetime

from crypto_sentiments.common.dateutils import daterange
from crypto_sentiments.models.models import CurrencyPrice
from crypto_sentiments.models.models import CurrencySentiment


DEFAULT_WINDOW_SIZE = 3
DIRECTIONS = set(['up', 'down', 'same'])


def feature_on(end, currency, window_size=DEFAULT_WINDOW_SIZE):
    """
    Creates a feature for a given date using window_size-1 number of previous
    dates from the database
    """
    if window_size < 2:
        raise Exception('Window size must be greater than 1')

    start = end - datetime.timedelta(days=window_size)
    csents = [
        CurrencySentiment.query.filter_by(
            currency=currency,
            date=d,
        ).first()
        for d in daterange(start, end)
    ]

    if len(csents) != window_size:
        raise Exception('Not enough data in database')

    sents = [csent.sentiment for csent in csents]
    return sum(sents) / len(sents)


def trainingset_between(start, end, currency, window_size=DEFAULT_WINDOW_SIZE):
    """
    Creates a training set between start and end, end exclusive using the given
    window_size
    """
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    training_set = []
    for d in daterange(start+datetime.timedelta(days=window_size), end):
        feature = feature_on(d, currency, window_size)
        p1 = CurrencyPrice.query.filter_by(
            currency=currency,
            date=d-datetime.timedelta(days=1),
        ).first().price
        p2 = CurrencyPrice.query.filter_by(currency=currency, date=d).first().price
        price_chg = p2 - p1

        if price_chg > 0:
            price_chg = 'up'
        elif price_chg < 0:
            price_chg = 'down'
        else:
            price_chg = 'same'

        training_set.append((feature, price_chg))

    return training_set
