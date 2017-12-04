# crypto_sentiments/common/dateutils.py

import datetime


def today():
    today = datetime.date.today()
    return datetime.datetime(today.year, today.month, today.day)

def daterange(start, end):
    if start <= end:
        for n in range((end - start).days):
            yield start + datetime.timedelta(n)
    else:
        daterange(end, start)
