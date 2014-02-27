# -*- coding: utf-8 -*-
"""code block for testing the twitter api"""
"""copied from http://grahamnic.wordpress.com/2013/09/15/python-using-the-twitter-api-to-datamine/"""
import re
import string
import nltk
from nltk.corpus import cmudict
import twitter
import curses
from curses.ascii import isdigit
#Setting up Twitter API
api = twitter.Api(
#insert your api info here
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
    no_at_sign = re.sub(r'\@\w+','',no_urls) #removes @ symbols and associated words
    no_punct = no_at_sign.translate(string.maketrans("",""), string.punctuation)
    no_RT = re.sub('RT|&amp','',no_punct)
    proper_spaces = re.sub(r'\s+',' ',no_RT)
    no_beginning = re.sub('^\s','',proper_spaces)
    no_unicode = no_beginning.decode('ascii', 'replace').replace(u'\ufffd', '')
    sentences = nltk.sent_tokenize(no_unicode) #breaks tweet into sentences
    return max(sentences, key=len) #returns sentence with the most characters
    
def process_tweet_unit_test():
    print process_tweet('Look at this @you #hashtag')
    print process_tweet("delete my final hashtagged words #swag #ewoifol #assnuts")
    print process_tweet("No bellboy? No problem! @book_exquisitetravels #adventure #destination #fun #igtravel #mytravelgram… http://t.co/9gLhXPDxvD")

def get_tweets_about(keyword, result_count):
    """returns a result_count length list of sentences from tweets that contain keyword"""
    search = api.GetSearch(term=keyword, lang='en', result_type='recent', count=result_count, max_id='')
    tweet_list = [] #we'll see if preallocation is neccessary... [None]*result_count
    for t in search:
         #Add the .encode to force encoding
         tweet = t.text.encode('utf-8')
         new_tweet = process_tweet(tweet)
         tweet_list.append(new_tweet)
    return tweet_list

def count_syllables_pseudo(word):
    """Uses an ad-hoc approach for counting syllables in a word
    copied straight from: http://allenporter.tumblr.com/post/9776954743/syllables"""
    vowel_list = ['a','e','i','o','u']
    def is_vowel(char):
        return char in vowel_list
    # Count the vowels in the word
    # Subtract one vowel from every dipthong
    count = len(re.findall(r'([aeiouyAEIOUY]+)', word))
    # Subtract any silent vowels
    if len(word) > 2:
        if word[-1] == 'e' and  \
        not is_vowel(word[-2]) and \
        is_vowel(word[-3]):
            count = count - 1
    return count
    
def count_syllables(word, dictionary):
    """returns number of syllables in a given word using CMU's syllable dictionary"""
    phenom_list = dictionary.get(word)
    if phenom_list == None:
        return count_syllables_pseudo(word)
    syllable_count = 0
    for phenom in phenom_list[0]:
        if isdigit(phenom[-1]): #cmu dictionary looks things up with 
            syllable_count+=1
    return syllable_count
    
def count_syllables_sentence(sentence,dictionary):  #pass in dictionary to avoid having to reinitialize it multiple times in order to increase speed
    """returns number of syllables in a sentence"""
    word_list = sentence.split()
    total_syllables = 0    
    for word in word_list:
        total_syllables+=count_syllables(word,dictionary)
    return total_syllables

def unit_test_count_syllables_sentence():
    dictionary = cmudict.dict()
    print count_syllables_sentence('hello please check my syllables',dictionary)
    print count_syllables_sentence('checking some syllables right now dog',dictionary)
        
def filter_tweets_by_syllables(tweet_list,min_syllable_count,max_syllable_count):
    """searches tweet_list and returns tweets with syllable count in specified range"""  
    filtered_list = []
    dictionary = cmudict.dict()
    for tweet in tweet_list:
        if min_syllable_count < count_syllables_sentence(tweet,dictionary) < max_syllable_count:
            filtered_list.append(tweet)
    return filtered_list
    
def filter_tweets_by_syllables_unit_test():
    tweet_list = get_tweets_about('nigga',20000)
    print filter_tweets_by_syllables(tweet_list,2,40)
    
    
def group_rhyming_tweets(filtered_tweet_list):
    """groups rhyming tweets into lists, then returns a list containing those lists. lists are sorted so that the list with the most rhyming words
    is first in the list."""
    return None
        
def get_rhyming_lines_about(keyword,min_line_length_syl,max_line_length_syl,tweets_to_search_through):
    """returns list of lists of grouped rhyming tweets, of specified line lengths. Searches through specified number of tweets to create this list."""
    tweet_list = get_tweets_about(keyword,tweets_to_search_through)
    return filter_tweets_by_syllables(tweet_list,min_line_length,max_line_length)
