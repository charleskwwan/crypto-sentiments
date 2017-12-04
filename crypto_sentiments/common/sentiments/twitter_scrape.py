"""
crypto_sentiments/common/scrape.py
https://github.com/taspinar/twitterscraper
"""

import re
import csv 
from urllib.parse import quote

# can raise 'fake_useragent.errors.FakeUserAgentError', if heroku site not good
import twitterscraper as ts


def _flatten_and_join(l, prefix, joiner):
    l = [prefix + w for w in re.split(r'\s', ' '.join(l)) if w != '']
    return joiner.join(l)


def twitter_query_string(
    required=[],
    phrases=[],
    optional=[],
    reject=[],
    hashtags=[],
    from_accs=[],
    to_accs=[],
    mention_accs=[],
    near=None,
    since=None,
    until=None,
):
    """
    Creates a twitter query string identical to that used in
    twitter.com/search-advanced

    Params:
    required [list[str]]: required words
    phrases [list[str]]: phrases, should contain quotes
    optional [list[str]]: optional words
    reject [list[str]]: unwanted words
    hashtags [list[str]]: hashtag words
    from_accs [list[str]]: from account names
    to_accs [list[str]]: to account names
    mention_accs [list[str]]: mentioned account names
    near [tuple(str, float)]: location string and radius distance in km
    since [datetime]: minimum year, month, day
    until [datetime]: maximum year, month, day

    Returns [str]: twitter query as URL string
    """    
    query_str = ''

    query_str += ' '.join(re.split(r'\s', ' '.join(required))) + ' '

    for p in phrases:
        query_str += '"{}" '.format(p)

    query_str += ' OR '.join(re.split(r'\s', ' '.join(optional))) + ' '
    query_str += _flatten_and_join(reject, '-', ' ') + ' '
    query_str += _flatten_and_join(hashtags, '#', ' OR ') + ' '
    query_str += _flatten_and_join(from_accs, 'from:', ' OR ') + ' '
    query_str += _flatten_and_join(to_accs, 'to:', ' OR ') + ' '
    query_str += _flatten_and_join(mention_accs, '@', ' OR ') + ' '

    if near:
        location, distance = near
        query_str += 'near:"{}" within:{}km'.format(location, distance) + ' '

    if since:
        query_str += 'since:{}-{}-{}'.format(
            since.year,
            since.month,
            since.day,
        ) + ' '

    if until:
        query_str += 'until:{}-{}-{}'.format(
            until.year,
            until.month,
            until.day,
        ) + ' '

    return quote(' '.join([w for w in re.split(r'\s', query_str) if w != '']))


def query_tweets(query, limit=None):
    """
    Wrapper over twitterscraper.query_tweets
    Note: anecdotally, twitter has an internal limit of about 20 values per
        field in the query string
    """
    tweets = ts.query_tweets(query, limit)
    return tweets


def prune_tweet(tweet):
    """
    Prunes a tweet in the following ways:
        1. Replace urls with the term URL
        2. Remove # from hashtags
        3. Replace account mentions in @... form with the term USER

    Params:
    s [str]: tweet text

    Returns [str]: pruned tweet text
    """
     # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    
    return tweet


def write_tweet(tweet): 
    """
    writes tweets handle, timestamp, and text to csv

    Params:
    s [obj]: tweet object

    Returns [None]: 
    """
    csvFile = open('./crypto_sentiments/data/cryptocurrency.csv', 'a')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow([tweet.fullname, tweet.timestamp, tweet.text])
