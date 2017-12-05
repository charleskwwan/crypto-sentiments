# crypto_sentiments/common/sentiment_tracking.py

import datetime
from concurrent.futures import ThreadPoolExecutor

from crypto_sentiments.common.constants import CURRENCIES
from crypto_sentiments.common.dateutils import daterange
from crypto_sentiments.common.dateutils import today
from crypto_sentiments.common.sentiments.twitter_scrape import prune_tweet
from crypto_sentiments.common.sentiments.twitter_scrape import query_tweets
from crypto_sentiments.common.sentiments.twitter_scrape import twitter_query_string
from crypto_sentiments.models import db
from crypto_sentiments.models.models import CurrencySentiment


_UNVERIFIED_ACCS = [
    'Skoylesy', 'jonmatonis', 'maxkeiser', 
    'stacyherbert', 'KonradSGraf', 'drwasho',
    'Goldcore', 'Cointelegraph', 'NickSzabo4',
    'jonmatonis', 'iamjosephyoung', 'CryptoCoinsNews',
    'CryptoBoomNews', 'CryptoCoiners', 'altcointoday',
]


class SentimentTracker(object):
    """
    """
    def __init__(
        self,
        classifier,
        start_date,
        pos='positive',
        neg='negative',
        neu='neutral',
        currencies=list(CURRENCIES.keys()),
    ):
        """
        Params:
        - classifier [obj]: trained tweet classifier, should have classify func
        - start_date [datetime]: date time from which to scrape tweets
            - highest allowed is today
        - pos [str]: classifier's positive sentiment tag
        - neg [str]: classifier's negative sentiment tag
        - neu [str]: classifier's neutral sentiment tag
        """
        self._classifier = classifier
        self._curr_date = min(today(), start_date)
        self._SENTS = {
            pos: 1,
            neg: -1,
            neu: 0,
        }
        self._currencies = set(currencies)

    def _scrape_tweets(self, currency, date, limit=1000):
        """
        Scrape tweets for a given currency on a specific date
        """
        tweets = []
        since, until = date, date + datetime.timedelta(days=1)

        # unverified accounts
        for i in range(int(len(_UNVERIFIED_ACCS)/15)+1): # chunk accs
            start = i * 15
            accounts = _UNVERIFIED_ACCS[start:start+15]
            if not accounts:
                break
            qs = twitter_query_string(
                required=[currency],
                from_accs=accounts, #temp
                since=since,
                until=until, # between start of days
                verified=False,
            )
            tweets.extend(query_tweets(qs, limit))

        # verified accounts
        qs = twitter_query_string(
            required=[currency],
            since=since,
            until=until,
            verified=True,
        )
        tweets.extend(query_tweets(qs, limit))

        return [prune_tweet(tweet.text) for tweet in tweets]

    def _aggregate_tweets_sentiment(self, tweets):
        """
        Computes an aggregate sentiment for a given list of tweets
        Sentiment is recorded -1 <= sentiment <= 1
        """
        sents = [
            self._SENTS[self._classifier.classify(tweet)]
            for tweet in tweets
        ]
        return sum(sents) / len(sents) if len(sents) > 0 else 0

    def track(self, until=None, override=False):
        """
        Pushes curr_date to until and processes tweets for all dates to until,
        excluding until
        
        Params:
        - until [datetime]: date of tweets to process until
            - default/highest possible is today
            - until must be greater than curr_date
        - override [bool]: if true, overrides existing entries in database
        """
        if until and until <= self._curr_date:
            return
        if not until or until > today():
            until = today()

        pool = ThreadPoolExecutor(max_workers=10)

        csents = []
        def calc_sentiment(csent, c, d):
            tweets = self._scrape_tweets(c, d)
            print('# Tracking sentiment on {} for {}: found {} tweets'.format(
                d.strftime('%Y-%m-%d'), 
                c,
                len(tweets),
            ))
            csent.sentiment = self._aggregate_tweets_sentiment(tweets)
            csents.append(csent)

        for d in daterange(self._curr_date, until):
            for c in self._currencies:
                csent = CurrencySentiment.query.filter_by(
                    currency=c,
                    date=d,
                ).first()

                if not override and csent:
                    return
                elif not csent:
                    csent = CurrencySentiment(currency=c, date=d)

                pool.submit(calc_sentiment, csent, c, d)
        pool.shutdown()

        for csent in csents:
            db.session.add(csent)
        db.session.commit()

        self._curr_date = until
