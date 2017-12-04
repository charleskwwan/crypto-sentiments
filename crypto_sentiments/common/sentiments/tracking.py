# crypto_sentiments/common/sentiment_tracking.py

import datetime

from crypto_sentiments.common.constants import CURRENCIES
from crypto_sentiments.common.sentiments.twitter_scrape import prune_tweet
from crypto_sentiments.common.sentiments.twitter_scrape import query_tweets
from crypto_sentiments.common.sentiments.twitter_scrape import twitter_query_string
from crypto_sentiments.models import db
from crypto_sentiments.models.models import CurrencySentiment


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
        self._curr_date = min(self._today(), start_date)
        self._SENTS = {
            pos: 1,
            neg: -1,
            neu: 0,
        }
        self._currencies = set(currencies)

    @staticmethod
    def _today():
        today = datetime.date.today()
        return datetime.datetime(today.year, today.month, today.day)

    @staticmethod
    def _daterange(start_date, end_date):
        """
        Generate dates from start to end, excluding end
        """
        if start_date <= end_date:
            for n in range((end_date - start_date).days):
                yield start_date + datetime.timedelta(n)
        else:
            SentimentTracker._daterange(end_date, start_date)

    def _scrape_tweets(self, currency, date, limit=2000):
        """
        Scrape tweets for a given currency on a specific date
        """
        qs = twitter_query_string(
            required=[currency],
            hashtags=[currency],
            from_accs=['CNBC', 'CNNMoney', 'WSJ', 'BTCTN', 'TechCrunch'], #temp
            since=date,
            until=(date + datetime.timedelta(days=1)), # between start of days
        )
        tweets = query_tweets(qs, limit)
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
        today = self._today()
        if not until or until > today:
            until = today

        for d in self._daterange(self._curr_date, until):
            for c in self._currencies:
                csent = CurrencySentiment.query.filter_by(
                    currency=c,
                    date=d,
                ).first()

                if not override and csent:
                    continue
                elif not csent:
                    csent = CurrencySentiment(currency=c, date=d)

                tweets = self._scrape_tweets(c, d)
                csent.sentiment = self._aggregate_tweets_sentiment(tweets)
                db.session.add(csent)

        db.session.commit()
        self._curr_date = until
