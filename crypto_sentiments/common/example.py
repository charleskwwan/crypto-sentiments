import datetime

from scrape import *


qstr = twitter_query_string(
    required=['bitcoin'],
    from_accs=['CNBC'],
    since=datetime.datetime(2015, 1, 1),
    until=datetime.datetime(2016, 12, 31),
)

tweets = query_tweets(qstr)

for t in tweets:
    print(t.fullname) # user
    print(t.timestamp) # date posted
    print(t.text) # tweet text, unpruned
    print() # newline
