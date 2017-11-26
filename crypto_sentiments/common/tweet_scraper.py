import tweepy
import csv
import pandas as pd
import re

####input your credentials here
consumer_key = 'enter-credentials'
consumer_secret = 'enter-credentials'
access_token = 'enter-credentials'
access_token_secret = 'enter-credentials'


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
    s = re.sub(r'\n', ' ', s)

    return s

def scrape(query, quantity, date): 
	"""
    Uses the tweepy api to scrape tweets and write tweets to csv
    
    Params:
    query [str]: words that must be in the tweet
    quantity [int]: number of tweets to scrape 
    date [str]: date of the earliest tweet ("yyyy-mm-dd")

    Returns: NA
    """

    # setup auth
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)

	# setup csv writer
	csvFile = open('./crypto_sentiments/data/cryptocurrency.csv', 'a')
	csvWriter = csv.writer(csvFile)

	for tweet in tweepy.Cursor(api.search, 
							   q=query,
							   count=quantity,
	                           lang="en",
	                           since=date).items():
		if quantity == 0: 
			break
		
		pruned_tweet = prune_tweet(tweet.text)
		csvWriter.writerow([str(tweet.created_at)[:10], pruned_tweet])
		quantity-=1  