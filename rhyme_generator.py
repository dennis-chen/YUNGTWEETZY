import math
import random

def verse_generator(rhymelist, segments = 4):
    """Generates a verse in a complete song.

    rhymelist: A list of lists of grouped tweet sentences.
    segments: How many groups of four lines would you like?
    """

    verse = []

    if segments == 0:
        return [verse,rhymelist]
    for segment in range(segments):

        # Create options that can be pulled into the rap.
        option1 = [rhyme for rhyme in rhymelist if len(rhyme) >= 4]
        option2 = [rhyme for rhyme in rhymelist if len(rhyme) >= 2 and len(rhyme) < 4]
        option3 = [rhyme for rhyme in rhymelist if len(rhyme) == 1]

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
            return "Ran out of options."

        # Make choice, add to verse, and remove from original.
        random_rhyme_choice = random.choice(options)
        if random_rhyme_choice == 'AAAA':
            AAAA = random.choice(option1)[0:4]
            verse = verse + AAAA
            for tweet in AAAA:
                for rhyme in rhymelist:
                    if tweet in rhyme:
                        rhyme.remove(tweet)
            print '1'

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
            print '2'

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
            print '3'

        elif random_rhyme_choice == 'ABCB':
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
            print '4'

        # print rhymelist
        # print verse

    return [verse, rhymelist]

def rap(rhymelist):
    """Creates the rap and saves it in a text file.

    rhymelist: A list of lists of grouped tweet sentences.
    """
    # Verse 1
    result = verse_generator(rhymelist)
    verse1 = result[0]
    rhymelist = result[1]

    # Hook
    result = verse_generator(rhymelist,2)
    hook = result[0]
    rhymelist = result[1]

    # Verse 2
    result = verse_generator(rhymelist)
    verse2 = result[0]
    rhymelist = result[1]

    # Verse 3
    result = verse_generator(rhymelist)
    verse3 = result[0]
    rhymelist = result[1]

    # Bridge (Optional)
    result = verse_generator(rhymelist,random.randint(0,2))
    bridge = result[0]
    rhymelist = result[1]

    rap = verse1 + [''] + hook + [''] + verse2 + [''] + hook + [''] + verse3 + [''] + bridge + [''] + hook
    for verse in rap:
        rap.write("%s\n" % verse)

if __name__ == "__main__":
    # print verse_generator([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
    print verse_generator([[
    "Hold up, wait a minute, all good just a week ago","Crew at my house and we party every weekend so","On the radio, that's my favorite song","Make me bounce around, like I don't know, like I won't be here long","Now the thrill is gone, got no patience, cause I'm not a doctor","Girl why is you lying, girl why you Mufasa","Yeah, mi casa su casa, got stripper like Gaza","Got so high off volcanoes, now the flow is so lava"],
    ["Yeah, we spit that saliva, iPhone got message from Viber",
    "Either the head is so hydra, or we let bygones be bygones",
    "My God, you pay for your friends? I'll take that as a compliment",
    "Got a house full of homies, why I feel so the opposite?",
    "Incompetent ain't the half of it",
    "Saturdays we're Young Lavish-ing",
    "Saddest shit, is I'm bad as it",
    "Beans they took from the cabinet (Whoa)",
    "Sorry, I'm just scared of the future",
    "til 3005, I got your back, we can do this, hold up"]])[0]