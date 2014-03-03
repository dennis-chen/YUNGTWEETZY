import math
import random
import private_twitter_test

def verse_generator(rhymelist, segments = 4):
    """Generates a verse in a complete song.

    rhymelist: A list of lists of grouped tweet sentences.
    segments: How many groups of four lines would you like?
    """
    copied_rhymelist = rhymelist[:]
    verse = []

    if segments == 0:
        return [verse,copied_rhymelist]
    for segment in range(segments):

        # Create options that can be pulled into the rap.
        option1 = [rhyme for rhyme in copied_rhymelist if len(rhyme) >= 4]
        option2 = [rhyme for rhyme in copied_rhymelist if len(rhyme) >= 2 and len(rhyme) < 4]
        option3 = [rhyme for rhyme in copied_rhymelist if len(rhyme) == 1]

        # options = ['AAAA','AABB','ABAB','ABCB']
        options = ['AAAA','AABB','ABAB']
        
        # Channel what is possible.
        if len(option1) == 0:
            options.remove('AAAA')
        if len(option1 + option2) <= 1:
            options.remove('AABB')
            options.remove('ABAB')
        # if len(option3) == 0:
        #     options.remove('ABCB')
        if len(options) == 0:
            return [["Ran out of options."],copied_rhymelist]

        # Make choice, add to verse, and remove from original.
        random_rhyme_choice = random.choice(options)
        if random_rhyme_choice == 'AAAA':
            AAAA = random.choice(option1)[0:4]
            verse = verse + AAAA
            for tweet in AAAA:
                for rhyme in copied_rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)

        elif random_rhyme_choice == 'AABB':
            AABB = random.sample(option1 + option2,2)
            verse = verse + AABB[0][0:2] + AABB[1][0:2]
            for tweet in AABB[0][0:2]:
                for rhyme in copied_rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
            for tweet in AABB[1][0:2]:
                for rhyme in copied_rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)

        elif random_rhyme_choice == 'ABAB':
            ABAB = random.sample(option1 + option2,2)
            verse = verse + ABAB[0][0:1] + ABAB[1][0:1] + ABAB[0][1:2] + ABAB[1][1:2]
            for tweet in ABAB[0][0:2]:
                for rhyme in copied_rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
            for tweet in ABAB[1][0:2]:
                for rhyme in copied_rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
    return [verse, copied_rhymelist]
        # elif random_rhyme_choice == 'ABCB':
            # AC = option3
            # ABCB = 
            # temp = random.sample(option1 + option2,2)
            # verse = verse + temp[0][0:1] + temp[1][0:1] + temp[2][1:2] + temp[1][1:2]
            # for temp in temp[0][0:2]:
            #     for rhyme in rhymelist:
            #         if tweet in rhyme:
            #             rhyme.remove(tweet)
            # for temp in temp[1][0:2]:
            #     for rhyme in rhymelist:
            #         if tweet in rhyme:
            #             rhyme.remove(tweet)


def rap(rhymelist,hooklist):
    """Creates the rap and saves it in a text file.

    rhymelist: A list of lists of grouped tweet sentences.
    """
    # Verse 1
    permanent_rhymelist = rhymelist[:]
    result = verse_generator(rhymelist)
    verse1 = result[0]
    #rhymelist = result[1]
    print "rhymelist1",rhymelist

    # Hook
    result = verse_generator(hooklist,2)
    hook = result[0]
    #rhymelist = result[1]

    # Verse 2
    second_rhymelist = permanent_rhymelist[:]
    result = verse_generator(permanent_rhymelist)
    verse2 = result[0]
    #rhymelist = result[1]
    print "rhymelist2",permanent_rhymelist

    # Verse 3
    result = verse_generator(second_rhymelist)
    verse3 = result[0]
    #rhymelist = result[1]
    print "rhymelist3",second_rhymelist

    # Bridge (Optional)
    result = verse_generator(permanent_rhymelist,random.randint(0,2))
    bridge = result[0]
    #rhymelist = result[1]

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

    f = open("./the_rap.txt","w")
    for verse in rap:
        f.write("%s\n" % verse)
    f.close()

    return rap

if __name__ == "__main__":
#    print rap([[str(i) for i in range(20)],[str(i) for i in range(21,40)],[str(i) for i in range(41,60)],[str(i) for i in range(61,80)]],[[str(i) for i in range(20)],[str(i) for i in range(21,40)],[str(i) for i in range(41,60)],[str(i) for i in range(61,80)]])
    rhyme_list = private_twitter_test.get_rhyming_lines_about('fuck',13,15,1000)
    #print rhyme_list
    hook_rhyme_list = private_twitter_test.get_rhyming_lines_about('shit',9,10,1000)
    print rap(rhyme_list,hook_rhyme_list) 
