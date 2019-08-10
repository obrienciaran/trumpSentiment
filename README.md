# trumpSentiment
A sentiment analysis of President Trump's tweets. 

Exploratory data analysis is performed on President Trump's tweets, incorporating the Twint tool.

Twint is an advanced Twitter scraping & OSINT tool written in Python that doesn't use Twitter's API, allowing you to scrape a user's followers, following, Tweets and more while evading most API limitations.  More information below. 

Use scrapeTweets.py to collect the latest 5000 Tweets from Trump, clean them, and save them down in a .csv format. Simple change the output path. 

Note: trumpSentimentWordCloud.py is a standalone module used to generate the word cloud. It undergoes a different cleaning process than that in scrapeTweets.py and is used solely for the purposes of creating the word cloud.

Twint info and installation process: 
https://github.com/twintproject/twint

Some code referenced from:

https://towardsdatascience.com/analyzing-tweets-with-nlp-in-minutes-with-spark-optimus-and-twint-a0c96084995f?gi=740ee6d31ebd

and

https://medium.com/@shsu14/introduction-to-data-science-custom-twitter-word-clouds-704ec5538f46
