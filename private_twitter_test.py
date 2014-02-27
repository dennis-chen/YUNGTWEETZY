# -*- coding: utf-8 -*-
"""code block for testing the twitter api"""
"""copied from http://grahamnic.wordpress.com/2013/09/15/python-using-the-twitter-api-to-datamine/"""
import re
from nltk import tokenize
import twitter
#Setting up Twitter API
api = twitter.Api(
    #insert public/private twitter keys here
 )
 
def process_tweet(tweet):
    """given a tweet string, removes hashtags at end of sentences, removes links, 
    removes hashtag symbols, and returns the longest sentence in the tweet as a string."""
    url_regex = r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*'
    no_urls = re.sub(url_regex, '', tweet)
    no_url_words = no_urls.split()
    while no_url_words[-1][0] == '#' or no_url_words[-1][0] == '@':
        no_url_words.pop() #removes # and @ words if they're at the end, they're less likely to be relevant
    no_urls = " ".join(no_url_words)
    no_symbols = re.sub(r'[#@]','',no_urls) #removes @ symbols and all other hashtags 
    sentences = tokenize.sent_tokenize(no_symbols) #breaks tweet into sentences
    return max(sentences, key=len) #returns sentence with the most characters
    
def process_tweet_unit_test():
    print process_tweet('Look at this @you #hashtag')
    print process_tweet("delete my final hashtagged words #swag #ewoifol #assnuts")
    print process_tweet("No bellboy? No problem! @book_exquisitetravels #adventure #destination #fun #igtravel #mytravelgram… http://t.co/9gLhXPDxvD")

def get_tweets_about(keyword, min_char_length,result_count):
    """returns a list of sentences from tweets that contain keyword and are longer than min_char_length"""
    search = api.GetSearch(term=keyword, lang='en', result_type='recent', count=result_count, max_id='')
    tweet_list = [] #we'll see if preallocation is neccessary... [None]*result_count
    for t in search:
         #Add the .encode to force encoding
         tweet = t.text.encode('utf-8')
         new_tweet = process_tweet(tweet)
         if len(new_tweet) > min_char_length:
             tweet_list.append(new_tweet)
    return tweet_list


