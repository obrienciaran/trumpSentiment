#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 10:42:49 2019

@author: Ciaran
"""

# Ensuring compatability with Python for Twint
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages")

# For cleaning the text
import re
from nltk.corpus import stopwords
import numpy as np

# For analysing Tweets
import collections

# For creating plots
import seaborn as sns
sns.set_style('darkgrid')

# For time series analysis
import pandas as pd

# For sentiment analysis
from textblob import TextBlob

# Clean Tweets
def cleanTweets(df):
    
    df["tweet"] = df["tweet"].apply(lambda x: x.lower())                               # Set to small case letters
    df["tweet"]= df["tweet"].str.replace('http\S+|www.\S+', '', case=False)            # Removing anything beginning with http
    df["tweet"]= df["tweet"].str.replace('https\S+|www.\S+', '', case=False)           # Removing anything beginning with https
    df["tweet"]= df["tweet"].str.replace('pic.twitter.com\S+|www.\S+', '', case=False) # Removing anything beginning with pic.twitter.com
    
    '''
    This regular expression uses 'look-behind' when removing hashtags.
    What this means is that any words which have a # in the middle will be kept. 
    Only words beginning with a hashtag are removed
    '''
    
    df["tweet"] = df["tweet"].str.replace('(?:(?<=\s)|(?<=^))#.*?(?=\s|$)', '', case=False) 
    df["tweet"] = df["tweet"].str.replace('(?:(?<=\s)|(?<=^))@.*?(?=\s|$)', '', case=False)     # Do the same as last line but for @ calls    
    df["tweet"] = df["tweet"].str.replace('[^\w\s]',' ')                               # Remove punctuation
    df["tweet"] = df["tweet"].str.replace('[^\w\s#@/:%.,_-]', '', flags=re.UNICODE)    # Remove emojis (unicode)
    df["tweet"] = df["tweet"].str.rstrip()                                             # Remove trailing whitespace to the left and right
    df["tweet"] = df["tweet"].str.lstrip()
    
    stopWords = stopwords.words('english')                                             # Remove stop words
    df["tweet"] = df["tweet"].apply(lambda x: ' '.join([word for word in x.split() if word not in (stopWords)]))
    
    df["tweet"] = df["tweet"] .str.replace("  "," ")                                   # Remove all the white space in between words
    
    df["tweet"].replace('', np.nan, inplace=True)                                      # Finally, after all this cleaning, some tweets are blank. Remove these.
    df.dropna(subset=["tweet"], inplace=True)
    
    return df

# get a word count per sentence column
def wordCount(sentence):
    return len(sentence.split())

'''
Note: I preffered Seaborn histograms but tried MatplotLib first.

import matplotlib.pyplot as plt
def wordFreq(df):
    plt.figure(figsize=(12,6))
    plt.xlim(0,45)
    plt.xlabel('word count')
    plt.ylabel('frequency')
    n,g = plt.hist(df["wordCount"],color='#0504aa', alpha=0.5,rwidth=0.85)
    plt.legend(loc='upper right')
    maxfreq = n.max()
    
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
'''   

# Textblob package has a pre-trained model for analysing sentiment
def analizeSentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob. 
    '''
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

def main():
    
#==============================================================================
#     EDA
#==============================================================================

    df = pd.read_csv(r"/Users/Ciaran/Desktop/Work/Code/Trump Tweets/trumpTweets.csv")
   
    # clean text. Note: we keep numeric characters in tweets as these may be of interest
    df = cleanTweets(df)

    # Number words per tweet.
    df["wordCount"] = df["tweet"].apply(wordCount)
    df.head(3)
    sns.distplot(df["wordCount"],kde=False,norm_hist=False) # With count on y axis
    sns.distplot(df["wordCount"],norm_hist=False)           # With normalised densities on y axis plus a trend line

    # Most popular words
    tweets = list(df["tweet"])
    tweets = ''.join(tweets)                               # join into one big string
    tweets = tweets.split()
    tweets = [w for w in tweets if len(w) > 2]             # ignore words which are two letters or fewer
    collections.Counter(tweets).most_common(20)

    # Tweets per year timeline. 
    tlen = pd.Series(data=df['wordCount'].values, index=df['date'])
    tlen.plot(figsize=(30,10), color='b');

    # Num tweets per month
    df['date'] = pd.to_datetime(df['date'])
    df.groupby([df['date'].dt.year.rename('year'), df['date'].dt.month.rename('month')]).agg({'count'})


    # Sentiment analysis
    
    #SA score . Bigger number means more positive 
    df.groupby([df['date'].dt.year.rename('year'), df['date'].dt.month.rename('month')]).agg({'sum'})

    df["SA"] = np.array([ analizeSentiment(tweet) for tweet in df["tweet"] ])
    pos, neu, neg = df['SA'].value_counts()
    pos/len(df["SA"]) * 100
    neu/len(df["SA"]) * 100
    neg/len(df["SA"]) * 100


if __name__ == '__main__':
    
    main()
    