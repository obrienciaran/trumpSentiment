#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 10:42:49 2019

@author: Ciaran
"""

'''
The Twint module would not import unless I appended the path it was stored in 
to the sys following the pip3 installation. 
'''

# Ensuring compatability with Python for Twint
import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages")

# For scraping tweets
import twint

# For cleaning the text
import re
from nltk.corpus import stopwords
import numpy as np

# initialise module
c = twint.Config()

# Twitter username
c.Username = "realDonaldTrump"

# Custom format ouput
c.Format = "Username: {username} |  Tweet: {tweet}"

# Number Tweets. Lets take the most recent 5,000
c.Limit = 5000

# Make comptatable with Pandas
c.Pandas = True

# Remove hashtags
c.Show_hashtags = False     

# Hide output from console while scraping tweets
c.Hide_output = True  

# Run search
twint.run.Search(c)

'''
Next two functions referenced from Favio Vazquez, with thanks, from:
https://towardsdatascience.com/analyzing-tweets-with-nlp-in-minutes-with-spark-optimus-and-twint-a0c96084995f?gi=740ee6d31ebd
'''

# Save into Pandas
def available_columns():
    return twint.output.panda.Tweets_df.columns

def twint_to_pandas(columns):
    return twint.output.panda.Tweets_df[columns]

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

def main(OUTPUTPATH):
    
    # Check available columns
    available_columns()
    
    # Convert to Pandas dataframe
    df = twint_to_pandas(["date", "tweet", "nlikes"])
  
#==============================================================================
#     Save df as CSV
#==============================================================================
    df.to_csv(OUTPUTPATH + "trumpTweets", index = False)

if __name__ == '__main__':
    
    OUTPUTPATH = r"/Users/Ciaran/Desktop/Work/Code/Trump Tweets/"

    main(OUTPUTPATH)
    