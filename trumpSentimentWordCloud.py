'''
Note: 
This is a standalone piece of code. It generates the tweets, cleans them, and generates the word cloud.
It does not output or save any files. 

If you do not want to generate word clouds, just use the scrapetweets.py file to generate Tweet data, 
and trumpSentimentAnalysis.py if you want to perform analysis on the tweets. 


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

# Generate a wordcloud
from scipy.misc import imread

from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt

# initialise module
c = twint.Config()

# Twitter username
c.Username = "realDonaldTrump"

# Custom format ouput
c.Format = "Username: {username} |  Tweet: {tweet}"

# Number Tweets. Lets take the most recent 5000
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

# Clean text for wordword generation
def cleanWordCloud(words):    
    words = ''.join(words)                               # join into one big string
    words = re.sub(r'http\S+', '', words)                # remove links
    words = re.sub(r"\\[a-z][a-z]?[0-9]+", '', words)    # remove unicode (emojis)
    words = re.sub('[^A-Za-z ]+', '', words)             # remove special characters
    words = words.split(" ")                             # process on word-by-word basis
    words = [w for w in words if len(w) > 2]             # ignore words which are two letters or fewer
    words = [w.lower() for w in words]
    return words
    
# Generate Word Cloud in Twitter shape
def wordCloudTwitter(words,MASKTWITTER):
    wc = WordCloud(background_color="white", max_words=200, mask=MASKTWITTER)
    clean_string = ','.join(words)
    wc.generate(clean_string)

    f = plt.figure(figsize=(25,25))
    f.add_subplot(1,2, 2)
    plt.imshow(wc, interpolation='bilinear')
    plt.title('Twitter Generated Cloud', size=20)
    plt.axis("off")
    plt.show()

# Generate Word Cloud in flag shape
def wordCloudFlag(words,MASKFLAG):
    wc = WordCloud(background_color="white", mode="RGB", max_words=1000, mask=MASKFLAG)
    clean_string = ','.join(words)
    wc.generate(clean_string)
    image_colors = ImageColorGenerator(MASKFLAG)
    plt.figure(figsize=[7,7],facecolor = 'white')
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")

def main(OUTPUTPATH,MASKTWITTER,MASKFLAG,OUTPUTTEXT):
    
    # Check available columns
    available_columns()
    
    # Convert to Pandas dataframe
    df = twint_to_pandas(["date", "tweet", "nlikes"])
    
    # Generate a Twitter logo and American flag shaped word cloud.s
    words = df["tweet"]
    words = cleanWordCloud(words)
    _wcTwitter = wordCloudTwitter(words,MASKTWITTER)
    _wcFlag = wordCloudFlag(words,MASKFLAG)

    # save all words used to generate the word cloud text to a .txt file 
    with open(OUTPUTTEXT, 'w') as file_handler:
        for word in words:
            file_handler.write("{}\n".format(word))
    
if __name__ == '__main__':
    
    OUTPUTPATH = r"/Users/Ciaran/Desktop/Work/"
    MASKTWITTER = imread(r'/Users/Ciaran/Desktop/Work/Code/Trump Tweets/twitter_mask.png',flatten=True)
   
    MASKFLAG = imread(r'/Users/Ciaran/Desktop/Work/Code/Trump Tweets/americanFlag.png', mode = "RGB")
    MASKFLAG = MASKFLAG.astype(int)

    OUTPUTTEXT = r"/Users/Ciaran/Desktop/Work/Code/Trump Tweets/trumpWordCloud.txt"
    
    main(OUTPUTPATH,MASKTWITTER,MASKFLAG,OUTPUTTEXT)
    
