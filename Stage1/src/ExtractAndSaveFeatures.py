#features are being extracted and saved along with labels for each possible candidate
#inputs: -> file numbers corresponding to train and test data
# 		 -> raw data without tagging, dictionary of candidate phrases along with their labels
# output: 2 feature files, one each corresponding to train and test	

import sys
import json
import pickle
import random
import hashlib
from FeatureExtraction import *
from sets import Set
from data.constants.commonSingleWord import *


def extractFeatures():
	print "***Extracting and saving features for train and test data***"
	for loop in range(2):
		if loop==0:
			with open('trainDataFileNumbers.txt', 'r') as file:	#file numbers of training data (was chosen randomly and saved)
		   		f1 = pickle.load(file)
		if loop==1:
	 		with open('testDataFileNumbers.txt', 'r') as file: #file numbers of test data (was chosen randomly and saved)
	 	  		f1 = pickle.load(file)

		inputFileList = []
		inputFileList.extend(f1)
		
		allFeatureList = []
		gtData = [] #ground truth data
		counter = 0	#counting total number of samples
		posCounter = 0 #counting number of positive examples
		for k in inputFileList:
			with open('./data/UnsupervisedData/%d.txt' % k,'r') as openfile:
				numCharacters=0 # number of total characters in the file
				the_whole_file = openfile.read()
				for line in the_whole_file:
					numCharacters += len(line)
				with open('./data/phraseDictData/%d.json' % k) as dictFile: 
					finalLengthWordDic = pickle.load(dictFile)
					lenWord = [1,2,3,4,5,6]
					for l in lenWord:
						for p in finalLengthWordDic[l]:
							counter = counter + 1
							phrase = p['string']
							startIdx = p['start_index']
							endIdx = p['end_index']
							label = p['label']
							currGTData = []
							currGTData.append(phrase)
							# currGTData.append(p)
							currGTData.append(k)
							# currGTData.append(l)
							gtData.append(currGTData)
							if label==1:
								posCounter = posCounter + 1
							entryFeatureList = []						
							entryFeatureList.append(isOfInThePhrase(phrase))
							entryFeatureList.append(isAndInThePhrase(phrase))
							
							# spclList = ['university', 'college', 'school', 'institute']
							entryFeatureList.append(isFirstWordInList(phrase))
							entryFeatureList.append(hasWordInSpclList(phrase))

							entryFeatureList.append(isAtBeforePhrase(the_whole_file, startIdx))
							entryFeatureList.append(isSecondWordBeforePhraseAt(the_whole_file, startIdx))

							entryFeatureList.append(isInBeforePhrase(the_whole_file, startIdx))
							entryFeatureList.append(isSecondWordBeforePhraseIn(the_whole_file, startIdx))
							
							entryFeatureList.append(isOfBeforePhrase(the_whole_file, startIdx))
							entryFeatureList.append(isSecondWordBeforePhraseOf(the_whole_file, startIdx))

							entryFeatureList.append(isTheBeforePhrase(the_whole_file, startIdx))
							
							# entryFeatureList.append(isPhraseAtTheBeginning(the_whole_file,startIdx))
							# entryFeatureList.append(isPhraseAtTheEnd(the_whole_file,endIdx,numCharacters))
							
							entryFeatureList.append(isFirstWordBeforePhraseCapitalized(the_whole_file,startIdx))
							entryFeatureList.append(isSecondWordBeforePhraseCapitalized(the_whole_file,startIdx))
							
							entryFeatureList.append(isFirstWordAfterPhraseCapitalized(the_whole_file,endIdx,numCharacters))
							# entryFeatureList.append(isSecondWordAfterPhraseCapitalized(the_whole_file,endIdx,numCharacters))
							
							entryFeatureList.append(isFirstWordBeforePhraseAAn(the_whole_file,startIdx))
							
							entryFeatureList.append(isSecondWordBeforePhraseProf(the_whole_file,startIdx))
							
							entryFeatureList.append(isFirstWordAfterPhraseAndFollowedByCapital(the_whole_file,endIdx,numCharacters))						
							entryFeatureList.append(isFirstWordAfterPhraseOfFollowedByCapital(the_whole_file,endIdx,numCharacters))
							
							entryFeatureList.append(isFirstWordAfterPhraseOf(the_whole_file,endIdx,numCharacters))
							
							# list = ["mr.", "mrs.", "dr.", "professor"]
							entryFeatureList.append(isFirstWordBeforePhraseInList(the_whole_file,startIdx))
							
							entryFeatureList.append(isAnyWordinCommomnSingleList(phrase,commonSingleWordUni))
							entryFeatureList.append(isWordinCommomnSingleList(phrase,commonSingleWordUni))
							
							entryFeatureList.append(isAllCaps(phrase))
							
							# entryFeatureList.append(isWordinCommomnSingleList(phrase,commonSingleWordUni))
							# entryFeatureList.append(isWordinCommomnSingleListHash(phrase,commonSingleWordUni))
							# entryFeatureList.append(isWordinCommomnSingleListHash(phrase,commonSingleWordUni))
							# entryFeatureList.append(isWordinCommomnSingleListHash(phrase,commonSingleWordUni))
							# entryFeatureList.append(isAnyWordinStateList(phrase,commonSingleWordUni))
							# entryFeatureList.append(isAnyWordinStateList(phrase, universityStates))

							entryFeatureList.append(label)			
							allFeatureList.append(entryFeatureList)
							
		if loop==0:
			print "\nTrainData: Total number of samples = ", counter
			print "TrainData: Number of positive samples = ", posCounter
			with open('featureDataTrain.txt', 'w') as f:
	   			f.write(json.dumps(allFeatureList))
			with open('gtDataTrain.txt', 'w') as f:
	   			f.write(json.dumps(gtData))
		if loop==1:	 
			print "\nTestData: Total number of samples = ", counter
			print "TestData: Number of positive samples = ", posCounter  			
			with open('featureDataTest.txt', 'w') as f:
		   		f.write(json.dumps(allFeatureList))
			with open('gtDataTest.txt', 'w') as f:
		   		f.write(json.dumps(gtData))

def main(argv):
	extractFeatures()
	
if __name__ == "__main__":
    main(sys.argv)