#input: takes unsupervised data and dictionary of positive samples as input (created in markup_PositiveEx)
# creates all possible candidates using n-grams from unsupervised data
# prunes out the negative examples using the rules that we have defined below
# output: Creates ans saves a dictionary of all remaining possible candidates with assigned 0/1 labels to them

import re
import sys
import pickle
import json

negNameList = ['college','school','high','university','institute','of','and']
university_preposition = ['of','and']
special_lowercase = ['of','and']
lengthOfWords = [1,2,3,4,5,6]

# The following 2 functions generates the strings of length 1 - 7.
def genWords(line, lenWord, startIndex, lengthStrings):
    #print line
    str = ''
    endIndex = 0
    for index in range(len(line)):
        str = ''
        if(index+lenWord <= len(line)):
            endIndex = startIndex
            for subIndex in range(index,index+lenWord):
                endIndex += len(line[subIndex])+1
                str = str + line[subIndex] + ' '
        str = str.strip()
        if(len(str) > 0):
            #print str
            lengthStrings.append({'string':str,'start_index':startIndex,'end_index':endIndex-2})
        startIndex += len(line[index])+1
    return startIndex, lengthStrings

def generateLengthWords(path, lenWord):
    try:
        file = open(path,"r")
        finalLengthWordDic = {}
        lengthStrings = []
        for l in lenWord:
            startIndex = 0
            lengthStrings = []
            for line in file:
                line = line.decode("utf-8").strip()
                startIndex, lengthStrings = genWords(re.findall(r'[.\w&]+',line),l,startIndex,lengthStrings)
            finalLengthWordDic[l] = lengthStrings
            file.seek(0)
        return finalLengthWordDic
    except IOError:
        print 'File does not exist'
    
# Pruning Rules for eliminating negative examples - 

# 1. Single Character in a string of length = 1
def pruneSingleCharString(finalLengthWordDic, startIndexDict):
    for index in reversed(range(len(finalLengthWordDic[1]))):
        if(len(finalLengthWordDic[1][index]['string']) == 1) or (len(finalLengthWordDic[1][index]['string']) == 2) :
            checkIfPositive(startIndexDict, finalLengthWordDic[1][index])
            del finalLengthWordDic[1][index]
    return finalLengthWordDic

# 2. Eliminate String with stop-word (.) in between
#    2.a Exactly 1 (.) in between
def pruneStopWordString(finalLengthWordDic, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            if len([m.start() for m in re.finditer('[A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]+[.]\s.+', finalLengthWordDic[l][index]['string'])]) == 1:
                #print finalLengthWordDic[l][index]['string'] 
                checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                del finalLengthWordDic[l][index]
    return finalLengthWordDic

# 3. Eliminate Strings as per the negative List 
def pruneRuleDelNeg(finalLengthWordDic, negStringList, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            for s in negStringList:
                if s in finalLengthWordDic[l][index]['string'].lower().split(' '):
                    #print finalLengthWordDic[l][index]['string'],s
                    checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                    del finalLengthWordDic[l][index]
                    break
    return finalLengthWordDic

# 4. Eliminate Strings with any words starting with lower letter 
def pruneSmallStartLetter(finalLengthWordDic, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            for string in finalLengthWordDic[l][index]['string'].split():
                    if string[0].islower() and string not in special_lowercase:
                        checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                        del finalLengthWordDic[l][index]
                        break
    return finalLengthWordDic
                
# 5. Eliminate Strings with numbers as individual words in between
def pruneNumberStrings(finalLengthWordDic, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            if re.match(r'.*[0-9]+.*',finalLengthWordDic[l][index]['string']):
                checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                del finalLengthWordDic[l][index]
    return finalLengthWordDic

# 6. Eliminate Strings of length = 1 and in negNameList
def pruneNegNameList(finalLengthWordDic, startIndexDict):
    for index in reversed(range(len(finalLengthWordDic[1]))):
        if finalLengthWordDic[1][index]['string'].lower() in negNameList:
            checkIfPositive(startIndexDict, finalLengthWordDic[1][index])
            del finalLengthWordDic[1][index]  
    return finalLengthWordDic

# 7. Eliminate Strings with first word in university_preposition
def pruneFirstWordPreposition(finalLengthWordDic, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            tempList = finalLengthWordDic[l][index]['string'].split(' ')
            if tempList[0].lower() in university_preposition or tempList[len(tempList)-1].lower() in university_preposition:
                checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                del finalLengthWordDic[l][index]
    return finalLengthWordDic

# 8. Eliminate Strings with two words from negNameList
def pruneTwoWordsNegName(finalLengthWordDic, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            tempList = finalLengthWordDic[l][index]['string'].split(' ')
            flag = False
            for string in tempList:
                if string.lower() in negNameList and string.lower() not in ['and','of','high']:
                    if flag == True:
                        checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                        del finalLengthWordDic[l][index]
                        break
                    else:
                        flag = True
    return finalLengthWordDic

# 9. Eliminate Strings with repeated words
def pruneStringRep(finalLengthWordDic, lenWord, startIndexDict):
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            tempList = finalLengthWordDic[l][index]['string'].split(' ')
            tempSet = set(tempList)
            if len(tempList) != len(tempSet):
                checkIfPositive(startIndexDict, finalLengthWordDic[l][index])
                del finalLengthWordDic[l][index]
                break
    return finalLengthWordDic

# Utility Methods

# Testing for not pruning out positive examples.
def checkIfPositive(startIndexDict, index):
    for (key,value) in startIndexDict.iteritems():
        if index['start_index'] == key and index['end_index'] == value['endIndex']:
            print 'Getting Deleted :', startIndexDict[index['start_index']]
        
def countTotalExamples(finalLengthWordDic, lenWord):
    count = 0
    for i in lenWord:
        count += len(finalLengthWordDic[i])
    print count
        
def generateWordList(path,lenWord):
    finalLengthWordDic = generateLengthWords(path,lenWord)
    countTotalExamples(finalLengthWordDic, lenWord)
    return finalLengthWordDic

def pruneNegatives(finalLengthWordDic, lenWord, startIndexDict):
    finalLengthWordDic = pruneSingleCharString(finalLengthWordDic, startIndexDict)
    finalLengthWordDic = pruneStopWordString(finalLengthWordDic,lenWord, startIndexDict)
    negFile = open('./data/constants/NegativeWordList.txt',"r")
    negStringList = negFile.read().split(',')
    finalLengthWordDic = pruneRuleDelNeg(finalLengthWordDic, negStringList, lenWord, startIndexDict)
    finalLengthWordDic = pruneSmallStartLetter(finalLengthWordDic, lenWord, startIndexDict)
    finalLengthWordDic = pruneNumberStrings(finalLengthWordDic, lenWord, startIndexDict) 
    finalLengthWordDic = pruneNegNameList(finalLengthWordDic, startIndexDict)
    finalLengthWordDic = pruneFirstWordPreposition(finalLengthWordDic, lenWord, startIndexDict)
    finalLengthWordDic = pruneTwoWordsNegName(finalLengthWordDic, lenWord, startIndexDict)
    finalLengthWordDic = pruneStringRep(finalLengthWordDic, lenWord, startIndexDict)
    return finalLengthWordDic

def printAllWords(finalLengthWordDic, lenWord):
    for i in lenWord:
        for j in finalLengthWordDic[i]:
            print j['string']

def labelExamples(startIndexDict, finalLengthWordDic, lenWord):
    count=0
    for l in lenWord:
        for index in reversed(range(len(finalLengthWordDic[l]))):
            for (key,value) in startIndexDict.iteritems():
                if finalLengthWordDic[l][index]['start_index'] == key:
                    if finalLengthWordDic[l][index]['end_index'] == value['endIndex']:
                        finalLengthWordDic[l][index]['label'] = 1
                        break
                else:
                    finalLengthWordDic[l][index]['label'] = 0
            else:
                finalLengthWordDic[l][index]['label'] = 0
    return finalLengthWordDic

def main(fileIndex):
    for k in fileIndex:
        try:
            with open('./data/positiveExamples/%d.json' % k,'r') as positive_file:
                stringPosList = pickle.load(positive_file)
                startIndexDict = {x['startIndex']: x for x in stringPosList['possamples']}
                path = './data/unsuperviseddata/%d.txt' % k
                print 'File is :',k,'.txt' 
                finalLengthWordDic = generateWordList(path, lengthOfWords)
                finalLengthWordDic = pruneNegatives(finalLengthWordDic, lengthOfWords, startIndexDict)
                countTotalExamples(finalLengthWordDic, lengthOfWords)
                finalLengthWordDic = labelExamples(startIndexDict, finalLengthWordDic, lengthOfWords)
                with open('./data/phraseDictData/%d.json' % k,'w') as dict_file:
                    pickle.dump(finalLengthWordDic, dict_file)
        except IOError:
            print 'File does not exist'

startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])
main(range(startIndex, endIndex))