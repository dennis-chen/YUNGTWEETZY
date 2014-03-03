# The MIT License (MIT)

# Copyright (c) 2013 Yat Choi

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import Wordsmith
import DataReader
import math
import time

Wordsmith.setup()

def rhyme(word, maxnum=75):
	rhymes = getNearRhymes(word.lower())

	output = []

	count = 0
	for i in range(len(rhymes)):
		output.append(rhymes[i][0])
		count += 1
		if count == maxnum:
			break

	return output
 
def get_rhyme_score(word1,word2):
    if word1 == word2:
        return 0
    pron1 = Wordsmith.tokenize(word1)
    pron2 = Wordsmith.tokenize(word2)
    return nearRhymeScore(pron1,pron2)

def getNearRhymes(inputString):
	rhymes = []
	pron1 = Wordsmith.tokenize(inputString)

	words = Wordsmith.getRelevantWords(inputString)
	if not words:
		return []

	for word in words:
		word = str(word)
		if inputString == word:
			continue
		elif "'" in word:
			continue

		pron2 = Wordsmith.tokenize(word)
		if not pron2:
			continue
		
		score = nearRhymeScore(pron1, pron2)
		if score > 0:
			rhymes.append((word, score))

	
	return sorted(rhymes, key=lambda t: t[1], reverse=True)

def nearRhymeScore(pron1, pron2):
	stress1 = Wordsmith.getStress(pron1)
	stress2 = Wordsmith.getStress(pron2)

	if not stress1 or not stress2:
		return -1

	if ((len(stress1) - len(stress2)) > 1):
		return -1

	match = 0

	if (len(stress1) > len(stress2)):
		tempStress = stress1
		stress1 = stress2
		stress2 = tempStress

		tempPron = pron1
		pron1 = pron2
		pron2 = tempPron

	for i in range(1,len(stress1)+1):
		

		# Check same stress pattern of word
		if (stress1[-i][0] == stress2[-i][0]):
			match+= 1

		score = nearSyllableScore(stress1[-i], stress2[-i])
		if (score < 0):
			match = -1
			break
		elif (i==1) and (score*1.5 < 1):
			match = -1
			break

		else:
			consonantScore = 0
			if (stress1[-i][2] > 0) and (stress2[-i][2] > 0) and (stress1[-i][2] < len(pron1) - 1) and (stress2[-i][2] < len(pron2)-1):
				index1 = stress1[-i][2]
				index2 = stress2[-i][2]

				# Check surrounding consonants for closeness
				consonantScore = nearConsonantScore(pron1[index1+1], pron2[index2+1])
			
			if i == 1:
				score *= 1.5
				if score > 1:
					consonantScore *= 2.5

				# if i == 2:
				# 	consonantScore *=1.5

			# print i
			# print stress1[-i]
			# print stress2[-i]
			# print score
			# print consonantScore

			match+= score
			match+= consonantScore

	return match

def check(inputString, word):
	if inputString == word:
		return -1

	pron1 = Wordsmith.tokenize(inputString)
	pron2 = Wordsmith.tokenize(word)

	print pron1
	print pron2
		
	return nearRhymeScore(pron1, pron2)

def nearSyllableScore(syllable1, syllable2):
	if ((syllable1[0] == syllable2[0]) and (syllable1[1] == syllable2[1])):
		return 2

	score = -1
	if (syllable1[1][:2] == syllable2[1][:2]):
		score = 1.8
	elif ((syllable1[1][:2] == 'IH' and syllable2[1][:2] == 'AH') or (syllable1[1][:2] == 'AH' and syllable2[1][:2] == 'IH')):
		score = 0.5
	elif ((syllable1[1][:2] == 'IH' and syllable2[1][:2] == 'IY') or (syllable1[1][:2] == 'IY' and syllable2[1][:2] == 'IH')):
		score = 0.3
	elif ((syllable1[1][:2] == 'AA' and syllable2[1][:2] == 'AO') or (syllable1[1][:2] == 'AO' and syllable2[1][:2] == 'AA')):
		score = 0.5
	elif ((syllable1[1][:2] == 'AH' and syllable2[1][:2] == 'AO') or (syllable1[1][:2] == 'AO' and syllable2[1][:2] == 'AH')):
		score = 0.5
	elif ((syllable1[1][:2] == 'AH' and syllable2[1][:2] == 'AY') or (syllable1[1][:2] == 'AY' and syllable2[1][:2] == 'AH')):
		score = 0.2
	elif ((syllable1[1][:2] == 'AY' and syllable2[1][:2] == 'AE') or (syllable1[1][:2] == 'AE' and syllable2[1][:2] == 'AY')):
		score = 0.5
	elif ((syllable1[1][:2] == 'AO' and syllable2[1][:2] == 'AE') or (syllable1[1][:2] == 'AE' and syllable2[1][:2] == 'AO')):
		score = 0.5
	elif ((syllable1[1][:2] == 'EY' and syllable2[1][:2] == 'AH') or (syllable1[1][:2] == 'AH' and syllable2[1][:2] == 'EY')):
		score = 0.25

	if (syllable1[0] == 1 and syllable2[0] == 1):
		score *= 0.25
	elif (syllable1[0] == 1 or syllable2[0] == 1):
		score *= 0.75
	elif(syllable1[0] != syllable2[0]):
		score *= 0.8

	return score

def nearConsonantScore(cons1, cons2):
	if (cons1 == cons2):
		return 1.2
	elif ((cons1 == 'T' and cons2 == 'D') or (cons1 == 'D' and cons2 == 'T')):
		return 1
	elif ((cons1 == 'S' and cons2 == 'Z') or (cons1 == 'Z' and cons2 == 'S')):
		return 1
	elif ((cons1 == 'S' and cons2 == 'T') or (cons1 == 'T' and cons2 == 'S')):
		return 0.4
	else:
		return 0


