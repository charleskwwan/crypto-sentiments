# crypto_sentiments/common/prices/tracking.py

import datetime
from concurrent.futures import ThreadPoolExecutor

from crypto_sentiments.common.constants import CURRENCIES # supported
from crypto_sentiments.common.dateutils import daterange
from crypto_sentiments.common.dateutils import today
from crypto_sentiments.common.prices.pricefinder import get_price
from crypto_sentiments.models import db
from crypto_sentiments.models.models import CurrencyPrice


class PriceTracker(object):
    """
    """
    def __init__(
        self,
        start_date,
        currencies=list(CURRENCIES.keys()),
    ):
        """
        Params:
        - start_date [datetime]: datetime from which to record prices
            - highest allowed is today
        - currencies [list[str]]: list of currencies to track
        """
        self._curr_date = min(today(), start_date)
        self._currencies = set(currencies)

    def track(self, until=None, override=False):
        """
        Pushes curr_date to until and saves prices for all dates to until,
        excluding until

        Params:
        - until [datetime]: date of prices to process until
            - default/highest possible is today
            - until must be greater than curr_date
        - override [bool]: if true, overrides existing entries in database
        """
        if until and until <= self._curr_date:
            return
        if not until or until > today():
            until = today()

        pool = ThreadPoolExecutor(max_workers=5)

        cprices = []
        def record_price(cprice, c, d):
            price = get_price(CURRENCIES[c], 'USD', d)
            print('# Tracking price on {} for {}'.format(d.strftime('%Y-%m-%d'), c))
            cprice.price = price
            cprices.append(cprice)

        for d in daterange(self._curr_date, until):
            for c in self._currencies:
                cprice = CurrencyPrice.query.filter_by(
                    currency=c,
                    date=d,
                ).first()

                if not override and cprice:
                    continue
                elif not cprice:
                    cprice = CurrencyPrice(currency=c, date=d)

                pool.submit(record_price, cprice, c, d)
        pool.shutdown()

        for cprice in cprices:
            db.session.add(cprice)
        db.session.commit()

        self._curr_date = until
