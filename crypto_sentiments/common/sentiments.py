# crypto_sentiments/common/sentiments.py

import argparse
import csv
import math
import pickle
import re
import time
from collections import Counter

import nltk
from nltk import ngrams
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords


def load_tweets_from_csv(
    fname,
    sent_header,
    text_header,
    pos_sent='pos',
    neg_sent='neg',
):
    """
    Loads tweets from a csv file

    Params:
    - fname [str]: file name
    - sent_header [str]: sentiment header
    - text_header [str]: tweet text header
    - pos_sent [str]: positive sentiment string in file
    - neg_sent [str]: negative sentiment string in file

    Returns [list[tuple[str, str]]]: list of tweets, each of which is a tuple of
        a tweet and a sentiment
    """
    tweets = []
    with open(fname, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[sent_header] == pos_sent:
                sentiment = 'pos'
            elif row[sent_header] == neg_sent:
                sentiment = 'neg'
            else:
                sentiment = None
            tweets.append((row[text_header], sentiment))
    return tweets


class TweetClassifier(object):
    """
    Twitter Classifier built on top of nltk's Naive Bayes Classifier
    """
    def __init__(self, tweets, percent=1):
        """
        Params:
        - tweets [list[tuple[tweet, sentiment]]]: list of tweets with their
            sentiments
        - percent [float]: percent of tweets to use, ranked by feature rareness
        """
        self.classifier = self._train(tweets, percent)


    @staticmethod
    def _filter(tweet, stops=stopwords.words('english')):
        """
        Filters a tweet for the feature vector in the following ways:
        - replace 2 or more repeats one char with the char itself
        - lowercase
        - strips punctuation
        - removes words that do not start with an alphabetic char 
        - removes stopwords

        Params:
        - tweet [str]: tweet string
        - stops [list[str]]: list of stop words

        Returns [str]: filtered tweet
        """
        stops = set(stops)
        stops.add(('AT_USER', 'URL'))
        # rep_pattern = re.compile(r"(.)\1{1,}", re.DOTALL)

        # tweet = rep_pattern.sub(r'\1\1', tweet)
        tweet = re.sub(r'(.)\1+', r'\1', tweet)
        words = [w for w in re.split(r'\s', tweet.lower()) if w != '']

        filtered = []
        for w in words:
            w = ''.join(re.findall(r'[\w-]+', w)) # only allow w chars or hyphens
            val = re.search(r"^[a-zA-Z].*$", w)
            if w not in stops and val != None:
                filtered.append(w)
        filtered = ' '.join(filtered)

        return filtered

    @staticmethod
    def _make_featureset(tweet, n=4):
        """
        Creates a feature set a given tweet

        Params:
        - tweet [str]: tweet string
        - n [int]: upper limit for ngrams

        Returns dict[?, int], ?]: featureset of ngrams to counts
        """
        words = tweet.split(' ')
        featureset = Counter()

        for i in range(n):
            grams = ngrams(words, i+1) if i > 0 else words
            for g in grams:
                featureset[g] += 1

        return dict(featureset)

    def _train(self, tweets, percent):
        """
        Trains Naive Bayes Classifier using tweets

        Params:
        - tweets [list[tuple[tweet, sentiment]]]: list of tweets with their
            sentiments
        - percent [float]: percent of tweets, ranked by rareness

        Returns [NaiveBayesClassifier]: classifier
        """
        # reduce tweets down to top ones with rarest words based on percent
        tweets = [(self._filter(tweet), sent) for tweet, sent in tweets]
        words = Counter([w for tweet, _ in tweets for w in tweet.split(' ')])
        words = sorted(list(words.items()), key=lambda x: x[1], reverse=True)
        words = {
            words[i][0]: 1/(len(words)-i+1) # small score best, +1 prevent div0
            for i in range(len(words))
        }

        ranked = []
        for tweet, sent in tweets:
            ws = set(tweet.split(' '))
            score = sum([words[w] for w in ws])
            ranked.append((score, (tweet, sent)))
        ranked.sort()

        tweets = [p for score, p in ranked[:int(len(ranked)*percent)]]
        del ranked, words # optimization

        # train
        trainingset = [
            (self._make_featureset(tweet), sent)
            for tweet, sent in tweets
        ]
        return NaiveBayesClassifier.train(trainingset)

    def classify(self, tweet):
        """
        Classifies a tweet using our classifier

        Params:
        - tweet [str]: tweet string

        Returns [?]: sentiment label
        """
        featureset = self._make_featureset(tweet)
        return self.classifier.classify(featureset)


def parse_args():
    parser = argparse.ArgumentParser(description='Create tweet classifier')
    parser.add_argument(
        'input',
        help='CSV input file',
    )
    parser.add_argument(
        'output',
        help='Output pickle file',
    )
    parser.add_argument(
        '--headers',
        help='Sentiment and Text headers for CSV file, in form <sent_header>,<text_header>',
        default='sentiment,text',
    )
    parser.add_argument(
        '--sents',
        help='Positive and Negative headers for CSV file, in form <pos_header>,<neg_header>',
        default='pos,neg',
    )
    parser.add_argument(
        '--percent',
        help='Percent of tweets to use',
        type=float,
        default=1,
    )

    args = parser.parse_args()

    m = re.match(r'(\w+),(\w+)', args.headers)
    if m:
        gs = m.groups()
        args.sent_header = gs[0]
        args.text_header = gs[1]
        del args.headers
    else:
        parser.error('--header needs arg in form of <sent_header>,<text_header>')

    m = re.match(r'(\w+),(\w+)', args.sents)
    if m:
        gs = m.groups()
        args.pos_header = gs[0]
        args.neg_header = gs[1]
        del args.sents
    else:
        parser.error('--sents needs arg in form of <pos_header>,<neg_header>')

    if args.percent < 0 or args.percent > 1:
        parser.error('--percent must be >=0 and <=1')

    return args


def main():
    args = parse_args()
    start_time = time.time()
    print('### Loading tweets from {}'.format(args.input))
    tweets = load_tweets_from_csv(
        args.input,
        args.sent_header,
        args.text_header,
        args.pos_header,
        args.neg_header,
    )

    print('### Training model')
    tc = TweetClassifier(tweets, args.percent)

    print('### Serialization object to {}'.format(args.output))
    with open(args.output, 'wb+') as f:
        pickle.dump(tc, f, protocol=pickle.HIGHEST_PROTOCOL)

    print('### Completed after: {} minutes'.format(
        round((time.time() - start_time)/60, 2),
    ))

if __name__ == '__main__':
    main()
