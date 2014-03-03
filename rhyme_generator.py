import math
import random
import rhyming_tweets
import copy

def verse_generator(rhymelist, segments = 4):
    """Generates a verse in a complete song.

    rhymelist: A list of lists of grouped tweet sentences.
    segments: How many groups of four lines would you like?
    """
    verse = []

    # Check to see if any segments are actually requested.
    if segments == 0:
        return verse
    
    # Loops through all the four bar segments requested.
    for segment in range(segments):

        # Create options that can be pulled into the rap.
        option1 = [rhyme for rhyme in rhymelist if len(rhyme) >= 4]
        option2 = [rhyme for rhyme in rhymelist if len(rhyme) >= 2 and len(rhyme) < 4]
        option3 = [rhyme for rhyme in rhymelist if len(rhyme) == 1]

        options = ['AAAA','AABB','ABAB']
        
        # Channel what is possible.
        if len(option1) == 0:
            options.remove('AAAA')
        if len(option1 + option2) <= 1:
            options.remove('AABB')
            options.remove('ABAB')
        if len(options) == 0:
            return ["Ran out of options."]

        # Make choice, add to verse, and remove from original.
        random_rhyme_choice = random.choice(options)
        if random_rhyme_choice == 'AAAA':
            AAAA = random.choice(option1)[0:4]
            verse = verse + AAAA
            for tweet in AAAA:
                for rhyme in rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
        elif random_rhyme_choice == 'AABB':
            AABB = random.sample(option1 + option2,2)
            verse = verse + AABB[0][0:2] + AABB[1][0:2]
            for tweet in AABB[0][0:2]:
                for rhyme in rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
            for tweet in AABB[1][0:2]:
                for rhyme in rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
        elif random_rhyme_choice == 'ABAB':
            ABAB = random.sample(option1 + option2,2)
            verse = verse + ABAB[0][0:1] + ABAB[1][0:1] + ABAB[0][1:2] + ABAB[1][1:2]
            for tweet in ABAB[0][0:2]:
                for rhyme in rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
            for tweet in ABAB[1][0:2]:
                for rhyme in rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
    
    return verse

def rap(rhymelist,hooklist):
    """Creates the rap and saves it in a text file.

    rhymelist: A list of lists of grouped tweet sentences.
    """

    # Verse 1
    verse1 = verse_generator(rhymelist)

    # Hook
    hook = verse_generator(hooklist,4)

    # Verse 2
    verse2 = verse_generator(rhymelist)

    # Verse 3
    verse3 = verse_generator(rhymelist)

    # Bridge (Optional)
    bridge = verse_generator(rhymelist,random.randint(0,2))

    # Append all of the rap into one complete list.
    rap = verse1 + [''] 
    rap += hook
    rap += ['']
    rap += verse2
    rap += ['']
    rap += hook
    rap += ['']
    rap += verse3
    rap += ['']
    rap += bridge
    rap += ['']
    rap += hook

    # Save rap into a text document.
    f = open("./the_rap.txt","w")
    for verse in rap:
        f.write("%s\n" % verse)
    f.close()

    return rap

if __name__ == "__main__":
#    print rap([[str(i) for i in range(20)],[str(i) for i in range(21,40)],[str(i) for i in range(41,60)],[str(i) for i in range(61,80)]],[[str(i) for i in range(20)],[str(i) for i in range(21,40)],[str(i) for i in range(41,60)],[str(i) for i in range(61,80)]])
    rhyme_list = rhyming_tweets.get_rhyming_lines_about('oscar',13,15,1000)
    print rhyme_list
    hook_rhyme_list = rhyming_tweets.get_rhyming_lines_about('movie',9,10,1000)
    print hook_rhyme_list
    print rap(rhyme_list,hook_rhyme_list) 