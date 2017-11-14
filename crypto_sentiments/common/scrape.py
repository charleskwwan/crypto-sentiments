"""
crypto_sentiments/common/scrape.py
https://github.com/taspinar/twitterscraper
"""

import re
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
    """
    return ts.query_tweets(query, limit)


def prune_tweet(s):
    """
    Prunes a tweet in the following ways:
        1. Replace urls with the term URL
        2. Remove # from hashtags
        3. Replace account mentions in @... form with the term USER

    Params:
    s [str]: tweet text

    Returns [str]: pruned tweet text
    """
    s = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', s)
    s = re.sub(r'#(\w+)', r'\1', s)
    s = re.sub(r'@(\w+)', 'USER', s)

    return s
