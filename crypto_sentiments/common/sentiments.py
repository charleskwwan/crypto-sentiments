# crypto_sentiments/common/sentiments.py

import argparse
import csv
import re
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
    """
    def __init__(self, tweets):
        """
        Params:
        - tweets [list[tuple[tweet, sentiment]]]: list of tweets with their
            sentiments
        """
        self.classifier = self._train(tweets)


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

    def _make_featureset(self, tweet, n=4):
        """
        Creates a feature set a given tweet

        Params:
        - tweet [str]: tweet string
        - n [int]: upper limit for ngrams

        Returns dict[?, int], ?]: featureset of ngrams to counts
        """
        words = self._filter(tweet).split(' ')
        featureset = Counter()

        for i in range(n):
            grams = ngrams(words, i+1) if i > 0 else words
            for g in grams:
                featureset[g] += 1

        return dict(featureset)

    def _train(self, tweets):
        """
        Trains Naive Bayes Classifier using tweets

        Params:
        - tweets [list[tuple[tweet, sentiment]]]: list of tweets with their
            sentiments

        Returns [NaiveBayesClassifier]: classifier
        """
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
