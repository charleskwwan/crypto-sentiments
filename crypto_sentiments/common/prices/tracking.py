# crypto_sentiments/common/prices/tracking.py

import datetime

from crypto_sentiments.common.constants import CURRENCIES # supported
from crypto_sentiments.common.dateutils import today
from crypto_sentiments.common.prices.pricefinder import get_price_in_range
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

        for c in self._currencies:
            code = CURRENCIES[c]
            prices = get_price_in_range(code, 'USD', self._curr_date, until)

            for price, d in prices:
                cprice = CurrencyPrice.query.filter_by(
                    currency=c,
                    date=d,
                ).first()

                if not override and cprice:
                    continue
                elif not cprice:
                    cprice = CurrencyPrice(currency=c, date=d)

                cprice.price = price
                db.session.add(cprice)

        db.session.commit()
