import math
import random
# from math.random import shuffle

def verse_generator(rhymelist, segments = 4):
    """Generates a verse in a complete song.

    rhymelist: A list of lists of grouped tweet sentences.
    segments: How many groups of four lines would you like?
    """

    verse = []

    


    for segment in range(segments):

        # Create options that can be pulled into the rap.
        option1 = [rhyme for rhyme in rhymelist if len(rhyme) >= 4]
        option2 = [rhyme for rhyme in rhymelist if len(rhyme) >= 2 and len(rhyme) < 4]
        option3 = [rhyme for rhyme in rhymelist if len(rhyme) == 1]

        options = ['AAAA','AABB','ABAB','ABCB']
        
        # Channel what is possible.
        if len(option1) == 0:
            options.remove('AAAA')
        if len(option2) == 0:
            options.remove('AABB')
            options.remove('ABAB')
        if len(option3) == 0:
            options.remove('ABCB')
        if len(options) == 0:
            return "Ran out of options."

        # 
        random_rhyme_choice = random.choice(options)
        if random_rhyme_choice == 'AAAA':
            print option1

        elif random_rhyme_choice == 'AABB':
            print '2'

        elif random_rhyme_choice == 'ABAB':
            print '3'

        elif random_rhyme_choice == 'ABCB':
            print '4'

    return verse

def rap():
    """Creates the rap and saves it in a text file.

    tweetlist: The complete list of tweets in their most processed form.
    rhymescheme: The rhymescheme generated earlier that will be used to compose our rap.
    """
    return None

if __name__ == "__main__":
    print verse_generator([[1,2,3,4],[5,6,7],['3'],['4']])