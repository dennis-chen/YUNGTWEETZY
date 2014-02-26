from pattern.web import Twitter
import time

# s = Twitter().stream('fail')
# for i in range(10):
#     time.sleep(1)
#     s.update(bytes=1024)
#     print s[-1].text if s else ''

if __name == "__main__":
    print hello
    
#import modules needed to pull tweets
#import python TLK probably to get rhyming words
#try using topsy and otter.topsy.com

def pull_tweets(keyword):
    """creates a textfile of tweets pulled using pattern's search engine function
    returns whatever the hell pattern or topsy or otter return
    """
    return None

def process_tweets(the_raw_tweets,shortest_tweet_length_allowed):
    """removes hashtags at end, removes links, and filters tweets that are too short
    return type is whatever it took as input"""
    return None
    
def group_rhyming_tweets(processed_tweets):
    """this will probably have to broken into a few more functions. takes tweets as input
    and returns a list of lists of tweets whose last words rhyme. The lists inside the list
    are sorted from largest to smallest."""
    return None
    
    