# Data Cleaning
# Input: rawdata files with tagging
# output: creates a clean raw data by removing unexpected characters and extra spaces.

import re
import sys

def change(m):
    return m.group(1) + m.group(2) + ' ' + m.group(3)

def countLines(open_file):
    count = 0
    for lines in open_file:
        lines = lines.decode('utf-8')
        matchObj = re.match(r'.*uname.*',lines)
        if matchObj:
            pass
        else:
            print lines
    open_file.seek(0)

def writeFile(fileIndex):
    for k in fileIndex:
        try:
            with open('./data/cleandata/clean_%d.txt' % k,'w') as output_file:
                with open('./data/rawdata/%d.txt' % k ,'r') as open_file:
                    #countLines(open_file)
                    openFile = open_file.read()
                    openFile = openFile.decode('utf-8').strip()
                    output_file.write(re.sub(r'([<>/\w&]+)([.])([<>/\w&]+)',change,openFile).encode('utf-8'))
        except IOError:
            print 'File does not exist'

startIndex = int(sys.argv[1])
endIndex = int(sys.argv[2])
writeFile(range(startIndex, endIndex))