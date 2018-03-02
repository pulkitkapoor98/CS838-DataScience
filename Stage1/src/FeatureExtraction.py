# library of features, all possible features have been defined here. 
# Not all features are being used. Check "ExtractAnsSaveFeatures.py" to see list of features being used

import sys
import hashlib
spclList = ['university', 'college', 'school', 'institute']

# is of in the phrase
def isOfInThePhrase(phrase):
	words = phrase.split();
	for word in words:	
		if word == "of":
			return 1
	return 0

def isAndInThePhrase(phrase):
	words = phrase.split();
	for word in words:	
		if word == "and":
			return 1
	return 0

def isFirstWordInList(phrase):
	words = phrase.split();
	if words[0].lower() in spclList:
		return 1
	else:
		return 0

def hasWordInSpclList(phrase):
	words = phrase.split();
	for word in words:
		if word.lower() in spclList:
			return 1
	return 0

#length of phrase
def lenOfPhrase(phrase):
	return len(phrase)

#number of strings in the phrase
def sizeOfPhrase(phrase):
	words = phrase.split()
	return len(words)

#is first character of each word capital except of "of"
#not being used...others pruned
def isFirstCharsCapital(phrase):
	words = phrase.split()
	i = 0
	n = len(words)
	for word in words:
		if word.lower() == ['of','in','for','at'] or word[0].isupper():
			i+=1
		else:
			break
	if i==n:
		return 1
	return 0
		

# is comma before last word	
# not using right now
def commaBeforeLastWord(phrase):
	idx = phrase.find(',')
	start = idx + 1
	end = len(phrase)
	word = phrase[start:end]
	words = word.split()
	if words == 1:
		return 1
	return 0


################ features using external information #########################
#######can use start and end index of the phrase for the information
### will need the raw file as input too ###

def isAtBeforePhrase(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-2].lower() == "at":
			return 1
		else:
			return 0
	else:
		return 0

def isSecondWordBeforePhraseAt(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-2][0].lower() == "at":
			return 1
		else:
			return 0
	else:
		return 0

def isInBeforePhrase(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-2].lower() == "in":
			return 1
		else:
			return 0
	else:
		return 0

def isSecondWordBeforePhraseIn(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-2][0].lower() == "in":
			return 1
		else:
			return 0
	else:
		return 0


def isOfBeforePhrase(openfile, startIdx):
	if startIdx<3:
		return 0
	else:
		data = openfile[startIdx-3:startIdx-2]
		if data.lower() == "of":
			return 1
		else:
			return 0

def isSecondWordBeforePhraseOf(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-2][0].lower() == "of":
			return 1
		else:
			return 0
	else:
		return 0


def isTheBeforePhrase(openfile, startIdx):
	if startIdx<4:
		return 0
	else:
		data = openfile[startIdx-4:startIdx-2]
		if data.lower() == "the":
			return 1
		else:
			return 0

#Is Phrase At The Beginning of the sentence
def isPhraseAtTheBeginning(openfile,startIdx):
	if startIdx<2:
		return 1
	else:
		if openfile[startIdx-2]==".":
			return 1
		else:
			return 0

#Is Phrase At The end of the sentence
#problem: will return true for U.C.L.A. even if not at the end of the sentence
def isPhraseAtTheEnd(openfile,endIdx,numCharacters):
	if endIdx==numCharacters-1:
		return 1
	else:
		if openfile[endIdx+1]==".":
			return 1
		else:
			return 0

def isFirstWordBeforePhraseCapitalized(openfile,startIdx):
	if startIdx>=20:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[-1][0].isupper():
			return 1
		else:
			return 0
	else:
		return 0

def isSecondWordBeforePhraseCapitalized(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-2][0].isupper():
			return 1
		else:
			return 0
	else:
		return 0


def isFirstWordAfterPhraseCapitalized(openfile,endIdx,numCharacters):
	if endIdx+20<numCharacters:
		substr = openfile[endIdx+1:endIdx+20].split()
		if substr[0][0].isupper():
			return 1
		else:
			return 0
	else:
		return 0

def isSecondWordAfterPhraseCapitalized(openfile,endIdx,numCharacters):
	if endIdx+40<numCharacters:
		substr = openfile[endIdx+1:endIdx+40].split()
		if substr[1][0].isupper():
			return 1
		else:
			return 0
	else:
		return 0

def isFirstWordBeforePhraseAAn(openfile,startIdx):
	if startIdx>=10:
		substr = openfile[startIdx-20:startIdx-1].split()
		if len(substr)>0:
			if substr[len(substr)-1].lower() == "a" or substr[len(substr)-1].lower() == "an":
				return 1
			else:
				return 0
		else:
			return 0
	else:
		return 0

def isFirstWordBeforePhraseProf(openfile,startIdx):
	if startIdx>=20:
		substr = openfile[startIdx-20:startIdx-1].split()
		if substr[len(substr)-1].lower() == "professor":
			return 1
		else:
			return 0
	else:
		return 0

def isSecondWordBeforePhraseProf(openfile,startIdx):
	if startIdx>=40:
		substr = openfile[startIdx-40:startIdx-1].split()
		if substr[len(substr)-2].lower() == "professor":
			return 1
		else:
			return 0
	else:
		return 0

def isFirstWordAfterPhraseAndFollowedByCapital(openfile,endIdx,numCharacters):
	if endIdx+40<numCharacters:
		substr = openfile[endIdx+1:endIdx+40].split()
		if substr[0].lower() == "and" and substr[1][0].isupper():
			return 1
		else:
			return 0
	else:
		return 0

def isFirstWordAfterPhraseOfFollowedByCapital(openfile,endIdx,numCharacters):
	if endIdx+40<numCharacters:
		substr = openfile[endIdx+1:endIdx+40].split()
		if substr[0].lower() == "of" and substr[1][0].isupper():
			return 1
		else:
			return 0
	else:
		return 0

def isFirstWordAfterPhraseOf(openfile,endIdx,numCharacters):
	if endIdx+20<numCharacters:
		substr = openfile[endIdx+1:endIdx+20].split()
		if substr[0][0].lower() == "of":
			return 1
		else:
			return 0
	else:
		return 0

def isFirstWordBeforePhraseInList(openfile,startIdx):
	if startIdx>=10:
		substr = openfile[startIdx-20:startIdx-1].split()
		if len(substr)>0:
			if substr[len(substr)-1].lower() in ['mr.', 'mrs.','dr.','professor']:
				return 1
			else:
				return 0
		else:
			return 0
	else:
		return 0

# list of single word common univ names
def isAnyWordinCommomnSingleList(phrase, uniNames):
	words = phrase.split()
	for word in words:
		if word in uniNames:
			return 1
	return 0

# def isAnyWordinCommomnSingleList(phrase, uniNames):
# 	words = phrase.split()
# 	flag = 0
# 	if len(words) > 1:
# 		for word in words:
# 			if word in uniNames and flag == 0:
# 				flag = 1
# 			else:
# 				return 0
# 	if flag == 1:
# 		return 1
# 	else:
# 		return 0

# if phrase has single word, from common uni names list ending with "."
def isWordinCommomnSingleList(phrase, uniNames):
	words = phrase.split()
	if len(words) == 1:
		if words[-1][-1] == '.':
			words[-1] = words[-1][:-1]
		if words[-1] in uniNames:
			return 1
	return 0
    
def isWordinCommomnSingleListHash(phrase, uniNames):
	words = phrase.split()
	if len(words) == 1:
		return int(hashlib.md5(words[-1]).hexdigest()[:8], 16)
	else:
		return 0

def isAnyWordinStateList(phrase, stateNames):
	words = phrase.split()
	flag = 0
	if len(words) > 1:
		for word in words:
			if word in stateNames:
				return 1
	return 0

# def isAnyWordinStateList(phrase, stateNames):
# 	words = phrase.split()
# 	flag = 0
# 	if len(words) > 1:
# 		for word in words:
# 			if word in stateNames and flag == 0:
# 				flag = 1
# 			else:
# 				return 0
# 	if flag == 1:
# 		return 1
# 	else:
# 		return 0

def isAllCaps(phrase):
	for c in phrase:
		if c.islower():
			return 0
	return 1