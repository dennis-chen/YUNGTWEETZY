# -*- coding: utf-8 -*-
"""code block for testing the twitter api"""
"""copied from http://grahamnic.wordpress.com/2013/09/15/python-using-the-twitter-api-to-datamine/"""
import re
import string
import nltk
from nltk.corpus import cmudict
import twitter
from curses.ascii import isdigit
import RhymeMaker #RhymeMaker is a python project by yat choi, we pulled from his github: https://github.com/yatchoi/rhymemaker
#Setting up Twitter API
api = twitter.Api(
 consumer_key='traZi7PRyq0tobvM4RCg',
 consumer_secret='kLkqEboCBCem2tjnFnauX7uclaejdgXSYjRvbCY',
 access_token_key='2363110866-svcxSbzzI82iKpQnGpJIQZv1HQppQN8urNTnOZ5',
 access_token_secret='dc56Cx1ulYZa2MjWWKFZk09nksKgpp8mjaUyFvMkztRFL'
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
    
def cut_tweet_to_syllables(tweet,syllable_cut_num,dictionary):
    """cuts the tweet down the appropriate number of syllables, using the syllable_cut_num as the minimum size it will return, since this function will not cut a word in half to get the right number of syllables."""
    word_list = tweet.split()
    syllable_target = syllable_cut_num
    new_tweet = []
    index = -1
    while syllable_target > 0:
        new_tweet.append(word_list[index])
        syllable_target = syllable_target - count_syllables(word_list[index],dictionary)
        index = index - 1
    new_tweet.reverse()
    new_tweet = ' '.join(new_tweet)
    return new_tweet

def cut_tweet_to_syllables_unit_test():
    dictionary = cmudict.dict()
    print cut_tweet_to_syllables('damn nigga look at all these syllables tho for real',10,dictionary)
    
#cut_tweet_to_syllables_unit_test()    
    
def filter_tweets_by_syllables(tweet_list,min_syllable_count,max_syllable_count):
    """searches tweet_list and returns tweets with syllable count in specified range"""  
    filtered_list = []
    dictionary = cmudict.dict()
    for tweet in tweet_list:
        if min_syllable_count < count_syllables_sentence(tweet,dictionary) < max_syllable_count:
            filtered_list.append(tweet)
        elif count_syllables_sentence(tweet,dictionary) > max_syllable_count:
            cut_tweet = cut_tweet_to_syllables(tweet,min_syllable_count,dictionary)
            filtered_list.append(cut_tweet)
    return filtered_list
        
def filter_tweets_by_syllables_unit_test():
    tweet_list = get_tweets_about('carrot',20)
    print filter_tweets_by_syllables(tweet_list,8,10)

#print do_syllables_match('AE0','AE1')

def does_rhyme(word_1,word_2,num_of_matching_end_syl):
    """returns whether two words rhyme, based on how many matching end syllables are needed to be considered a 'rhyme' (typically two)
    returns False if it can't find one of the words in the dictionary."""
    entries = nltk.corpus.cmudict.entries()
    syllables_1 = [syl for word, syl in entries if word == word_1]
    syllables_2 = [syl for word, syl in entries if word == word_2]
    if len(syllables_1) == 0 or len(syllables_2) == 0:
        return False
    return do_syllables_match(syllables_1[0][-num_of_matching_end_syl:], syllables_2[0][-num_of_matching_end_syl:])

def does_rhyme_unit_test():
    print does_rhyme('lol','bol',2)  
    print does_rhyme('cat','dog',2)
    print does_rhyme('cat','bat',2)
    print does_rhyme('cat','tot',2)
    print does_rhyme('cat','tot',2)
    print does_rhyme('hello','yellow',2)
    
# print does_rhyme_unit_test()
    
def sentence_does_rhyme(sentence_1,sentence_2,num_of_matching_end_syl):
    return does_rhyme(sentence_1.split()[-1],sentence_2.split()[-1],num_of_matching_end_syl)
    
def sentence_rhyme_score(sentence_1,sentence_2):
    return RhymeMaker.get_rhyme_score(sentence_1.split()[-1],sentence_2.split()[-1])
    
def sentence_rhyme_score_unit_test():
    print sentence_rhyme_score('oh hello','no yellow')
    print sentence_rhyme_score('so the dog','log')
    print sentence_rhyme_score('potato','wefo')
    print sentence_rhyme_score('hog','log')
    print sentence_rhyme_score('potato','nose')
    print sentence_rhyme_score('hello','quote')
    print sentence_rhyme_score(u"I never finished watching slum dog millionaire", u"all niggas is dog but i be cheating myself")
    
#sentence_rhyme_score_unit_test()

def group_rhyming_tweets(filtered_tweet_list):
    """groups rhyming tweets into lists, then returns a list containing those lists. lists are sorted so that the list with the most rhyming words
    is first in the list."""
    copy_filtered_tweet_list = list(filtered_tweet_list)
    grouped_rhyming_tweets = []
    index = 0
    while index < len(copy_filtered_tweet_list)-1: #don't need to check last element for rhymes against other words b/c all pairs of words checked already by that point
        rhyme_list = [copy_filtered_tweet_list[index]]        
        i = index+1
        while i < len(copy_filtered_tweet_list):
            if sentence_rhyme_score(copy_filtered_tweet_list[index],copy_filtered_tweet_list[i]) >= 4:
                rhyme_list.append(copy_filtered_tweet_list[i])
                copy_filtered_tweet_list.pop(i)
                i = i-1
            i = i+1
        rhyme_list = list(set(rhyme_list)) #remove non-unique entries by converting to a set and back again
        grouped_rhyming_tweets.append(rhyme_list)
        index = index +1
    #grouped_rhyming_tweets = sorted(grouped_rhyming_tweets, key = len, reverse = True)
    grouped_rhyming_tweets = [i for i in grouped_rhyming_tweets if len(i) > 1]
    return grouped_rhyming_tweets     
       
def group_rhyming_tweet_unit_test():
    print group_rhyming_tweets(['oh hello','no yellow','so the dog','hog','nose','log','potato','wefo','nog'])
    
#group_rhyming_tweet_unit_test()
        
def get_rhyming_lines_about(keyword,min_line_length_syl,max_line_length_syl,tweets_to_search_through):
    """returns list of lists of grouped rhyming tweets, of specified line lengths. Searches through specified number of tweets to create this list."""
    tweet_list = get_tweets_about(keyword,tweets_to_search_through)
    filtered_tweets = filter_tweets_by_syllables(tweet_list,min_line_length_syl,max_line_length_syl)
    return group_rhyming_tweets(filtered_tweets)

#print get_rhyming_lines_about('dog',10,15,2000)


#NOTE: the code below was written originally to determine if words rhymed, but it turns out that the module we downloaded is just way more sophisticated and better at finding rhymes.
#def do_syllables_match(syl_list_1,syl_list_2):
#    for i in range(len(syl_list_1)):
#        syl_1 = re.sub('[0-9]$','',syl_list_1[i])
#        syl_2 = re.sub('[0-9]$','',syl_list_2[i])
#        if syl_1 != syl_2:
#            return False
#    return True
#
#def does_rhyme(word_1,word_2,num_of_matching_end_syl):
#    """returns whether two words rhyme, based on how many matching end syllables are needed to be considered a 'rhyme' (typically two)
#    returns False if it can't find one of the words in the dictionary."""
#    entries = nltk.corpus.cmudict.entries()
#    syllables_1 = [syl for word, syl in entries if word == word_1]
#    syllables_2 = [syl for word, syl in entries if word == word_2]
#    if not syllables_1 or not syllables_2:
#        return False
#    print syllables_1[0][-num_of_matching_end_syl:]
#    print syllables_2[0][-num_of_matching_end_syl:]
#    return do_syllables_match(syllables_1[0][-num_of_matching_end_syl:],syllables_2[0][-num_of_matching_end_syl:])
#    
#def does_rhyme_unit_test():
#    print does_rhyme('lol','bol',2)  
#    print does_rhyme('cat','dog',2)
#    print does_rhyme('cat','bat',2)
#    print does_rhyme('cat','tot',2)
#    print does_rhyme('cat','tot',2)
#    print does_rhyme('hello','yellow',2)
#    
#    
#sentence_does_rhyme_unit_test()