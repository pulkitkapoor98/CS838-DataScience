#input: this code takes clean data files as input
#output: -> creates a new file for each of the clean data by removing tags from the data. We call it unsupervised data
#        -> creates a dictionary of positive samples and stores in a file (phrase, start index, end index)

#note: all processing happens filewise

import sys
import re
import pickle

startTag = '<uname>'
endTag = '</uname>'

startTagSize = 7
endTagSize = 8

# Utility Functions
def change(m):
    return m.group(2) + m.group(4)

# The following 2 functions reads raw input and writes formatted output to a new file. 
# It as well notes down the positive examples and their positions.
def genWords(line, startIndex, output_file, positive_file, finalPosDict):
    str = ''
    endIndex = startIndex
    index = 0
    while (index < len(line)):
        if line[index].find(startTag) != -1:
            str = ''
            markedStartIndex = startIndex
            while(line[index].find(endTag) == -1):
                endIndex = startIndex + len(line[index]) - 1
                str += line[index] + ' '
                index = index + 1
                startIndex = endIndex + 2
            str = str + line[index]
            endIndex = startIndex + len(line[index]) - 1
            finalString = re.sub(r'(<uname>)(.+)(</uname>)(.*)',change,str)
            startIndex = markedStartIndex
            endIndex = startIndex + len(str) - 1 - startTagSize - endTagSize
            #print finalString, markedStartIndex, endIndex
            stringList = {}
            stringList['string'] = finalString
            stringList['startIndex'] = markedStartIndex
            stringList['endIndex'] = endIndex    
            finalPosDict['possamples'].append(stringList)
            #positive_file.write(unicode(stringList))
            output_file.write(finalString.encode('utf-8') + ' ')
        else:
            endIndex = startIndex + len(line[index]) - 1
            #print line[index], startIndex, endIndex
            output_file.write(line[index].encode('utf-8')+ ' ')
        startIndex = endIndex + 2
        index = index + 1
    return startIndex    

def readWriteFiles(fileNum):
    for k in fileNum:
        finalPosDict = {}
        finalPosDict['possamples'] = []
        try:
            with open('./data/positiveExamples/%d.json' % k,'w') as positive_file:
                with open('./data/unsuperviseddata/%d.txt' % k,'w') as output_file:      # creating the raw file without tags
                    with open('./data/cleandata/clean_%d.txt' % k ,'r') as open_file:      # input file
                        lengthStrings = []
                        startIndex = 0
                        for line in open_file:
                            line = line.decode('utf-8').strip()
                            #print line
                            startIndex = genWords(re.findall(r'[.<>/\w&]+',line), startIndex, output_file, positive_file, finalPosDict)
                pickle.dump(finalPosDict, positive_file)
        except IOError:
            print 'File does not exist'

startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])              
readWriteFiles(range(startIndex, endIndex))
            