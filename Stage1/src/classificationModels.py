#code to run cross validation on train data and testing on test data
# 5 models are being used: SVM,RF,Decision Tree, Linear regression, Logistic regression
# pass argument "train" to run CV and "test" to run testing
# no argument runs both sequentially 

import sys
import json
import numpy as np
from sklearn import tree
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model

# method to calculate precision, recall and f1 score
def calculatePRF1(y_test,y_pred):
    P = precision_score(y_test, y_pred)
    R = recall_score(y_test, y_pred)
    F1 = f1_score(y_test, y_pred)
    # print "\nprecision = ", P,", recall = " , R,", F1 score = ",F1
    return P,R,F1
 
def analyzeFalsePos(y_test, y_pred, test_indices, gtData):
	print "Analyzing False positives"
	for i in range(0,len(y_test)):
		if y_test[i] == 0:
			if y_test[i] != y_pred[i]:
				print gtData[test_indices[i]], y_test[i], y_pred[i]

def analyzeFalseNeg(y_test, y_pred, test_indices, gtData):
	print "Analyzing False negatives"
	for i in range(0,len(y_test)):
		if y_test[i] == 1:
			if y_test[i] != y_pred[i]:
				print gtData[test_indices[i]], y_test[i], y_pred[i]

def performCrossValidation(clf,X,y, k,gtData):
    averagePrec = 0
    averageRecall = 0
    kf = cross_validation.KFold(len(y), n_folds=k,random_state = None)
    foldcount = 1
    for train_index, test_index in kf:
    	# print "\nFold = ", foldcount
    	foldcount = foldcount + 1
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        # analyzeFalsePos(y_test,y_pred,test_index,gtData)
        # analyzeFalseNeg(y_test,y_pred,test_index,gtData)
        # print confusion_matrix(y_test,y_pred)
        P,R,F1 = calculatePRF1(y_test,y_pred)
        averagePrec = averagePrec + P
        averageRecall = averageRecall + R
    averagePrec = averagePrec/k
    averageRecall = averageRecall/k

    print "averagePrec = ", averagePrec, "averageRecall = ", averageRecall, "using",k,  "fold\n"

    # doing cross validation using method 2
    # y_pred = cross_val_predict(clf,X,y,cv=2*k)
    # P,R,F1 = calculatePRF1(y,y_pred)
    # # print confusion_matrix(y_test,y_pred)
    # print "\naveragePrec = ", P, "averageRecall = ", R, "using",2*k,  "fold (method 2)\n"


def performCrossValidationForLinReg(clf,X,y, k,gtData):
    averagePrec = 0
    averageRecall = 0
    kf = cross_validation.KFold(len(y), n_folds=k,random_state = None)
    foldcount = 1
    for train_index, test_index in kf:
    	# print "\nFold = ", foldcount
    	foldcount = foldcount + 1
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        clf.fit(X_train, y_train)
        predictions = clf.predict(X_test)
        y_pred = []
        for pred in predictions:
	        if pred > 0.5:
	            y_pred.append(1)
	        else:
	            y_pred.append(0)
        # analyzeFalsePos(y_test,y_pred,test_index,gtData)
        # analyzeFalseNeg(y_test,y_pred,test_index,gtData)
        # print confusion_matrix(y_test,y_pred)
        P,R,F1 = calculatePRF1(y_test,y_pred)
        averagePrec = averagePrec + P
        averageRecall = averageRecall + R
    averagePrec = averagePrec/k
    averageRecall = averageRecall/k

    print "averagePrec = ", averagePrec, "averageRecall = ", averageRecall, "using",k,  "fold\n"

    # doing cross validation using method 2
    # y_pred = cross_val_predict(clf,X,y,cv=2*k)
    # P,R,F1 = calculatePRF1(y,y_pred)
    # # print confusion_matrix(y_test,y_pred)
    # print "\naveragePrec = ", P, "averageRecall = ", R, "using",2*k,  "fold (method 2)\n"


#classification using Decision Tree
def runDecisionTree(X,y, gtData):
	print "\nRunning Decision Tree"
	clf = tree.DecisionTreeClassifier(max_depth = 5, min_samples_leaf = 3)
	performCrossValidation(clf,X,y,5,gtData)


#classification using Random Forest
def runRandomForest(X, y, gtData):
	print "\nRunning RF"
	clf = RandomForestClassifier(max_depth=10, random_state=0,class_weight = {0:.4, 1:.6})
	performCrossValidation(clf,X,y,5,gtData)


#classification using Linear Regression
def runLinearReg(X, y, gtData):
	print "\nRunning Linear Regression"
	clf = linear_model.LinearRegression()
	performCrossValidationForLinReg(clf,X,y,5,gtData)


#classification using Logistic Regression
def runLogisticReg(X,y,gtData):
    print "\nRunning Logistic Regression"
    clf = LogisticRegression(C=1, penalty='l1')
    performCrossValidation(clf,X,y,5,gtData)


def runSVM(X, y, gtData):
	print "\nRunning SVM"
	clf = svm.SVC(C = 10, kernel='rbf', gamma = .5,class_weight = {0:.5, 1:.5})
	performCrossValidation(clf,X,y,5,gtData)



def runSVMTest(XTrain, yTrain, gtDataTrain,XTest,yTest,gtDataTest):
	print "\nRunning SVM"
	clf = svm.SVC(C = 10, kernel='rbf', gamma = .5)
	clf = clf.fit(XTrain, yTrain)
    
	y_pred  = clf.predict(XTest)
    # print confusion_matrix(yTest, y_pred)
	P,R,F1 = calculatePRF1(yTest,y_pred)
	print "Test precision = ", P,", Test recall = " , R,", Test F1 score = ",F1

    # analyzeFalsePos(yTest,y_pred,range(0,len(yTest)),gtDataTest)
    # analyzeFalseNeg(y_test,y_pred,test_indices,gtData)

def runRFTest(XTrain, yTrain, gtDataTrain,XTest,yTest,gtDataTest):
	print "\nRunning RF"
	clf = RandomForestClassifier(max_depth=10, random_state=0,class_weight = {0:.4, 1:.6})
	clf = clf.fit(XTrain, yTrain)
    
	y_pred  = clf.predict(XTest)
    # print confusion_matrix(yTest, y_pred)
	P,R,F1 = calculatePRF1(yTest,y_pred)
	print "Test precision = ", P,", Test recall = " , R,", Test F1 score = ",F1

    # analyzeFalsePos(yTest,y_pred,range(0,len(yTest)),gtDataTest)
    # analyzeFalseNeg(y_test,y_pred,test_indices,gtData)

def runDTTest(XTrain, yTrain, gtDataTrain,XTest,yTest,gtDataTest):
	print "\nRunning Decision Tree"
	clf = tree.DecisionTreeClassifier(max_depth = 5, min_samples_leaf = 3)
	clf = clf.fit(XTrain, yTrain)
    
	y_pred  = clf.predict(XTest)
    # print confusion_matrix(yTest, y_pred)
	P,R,F1 = calculatePRF1(yTest,y_pred)
	print "Test precision = ", P,", Test recall = " , R,", Test F1 score = ",F1

    # analyzeFalsePos(yTest,y_pred,range(0,len(yTest)),gtDataTest)
    # analyzeFalseNeg(y_test,y_pred,test_indices,gtData)


def runLinRegTest(XTrain, yTrain, gtDataTrain,XTest,yTest,gtDataTest):
	print "\nRunning Linear Regression"

	clf = linear_model.LinearRegression()
	clf = clf.fit(XTrain, yTrain)

	predictions  = clf.predict(XTest)

	y_pred = []
	for pred in predictions:
		if pred > 0.5:
			y_pred.append(1)
		else:
			y_pred.append(0)

	# print confusion_matrix(yTest, y_pred)
	P,R,F1 = calculatePRF1(yTest,y_pred)
	print "Test precision = ", P,", Test recall = " , R,", Test F1 score = ",F1

	# analyzeFalsePos(yTest,y_pred,range(0,len(yTest)),gtDataTest)
	# analyzeFalseNeg(y_test,y_pred,test_indices,gtData)


def runLogRegTest(XTrain, yTrain, gtDataTrain,XTest,yTest,gtDataTest):
	print "\nRunning Logistic Regression"
   	clf = LogisticRegression(C=1, penalty='l1')
	clf = clf.fit(XTrain, yTrain)
    
	y_pred  = clf.predict(XTest)
    # print confusion_matrix(yTest, y_pred)
	P,R,F1 = calculatePRF1(yTest,y_pred)
	print "Test precision = ", P,", Test recall = " , R,", Test F1 score = ",F1

    # analyzeFalsePos(yTest,y_pred,range(0,len(yTest)),gtDataTest)
    # analyzeFalseNeg(y_test,y_pred,test_indices,gtData)


# using train data to create model and testing on test data
def runTestClassification():
	print "\n*** Running test data classificaion ***"
	#loading train data
	with open('gtDataTrain.txt', 'r') as f:
		gtDataTrain = json.loads(f.read())

	with open('featureDataTrain.txt', 'r') as f:
		allFeatureList = json.loads(f.read())
        numInstances = len(allFeatureList)
        numFeatures = len(allFeatureList[0])
        print "Number of training instances: ", numInstances, "Number of features: ", numFeatures
        data = np.array(allFeatureList)
        XTrain = data[:,0:numFeatures-1]
        yTrain = data[:,numFeatures-1]

	with open('gtDataTest.txt', 'r') as f:
   		gtDataTest = json.loads(f.read())

	with open('featureDataTest.txt', 'r') as f:
		allFeatureList = json.loads(f.read())
		numInstances = len(allFeatureList)
		numFeatures = len(allFeatureList[0])
		print "Number of test instances: ", numInstances, "Number of features: ", numFeatures
		data = np.array(allFeatureList)
		XTest = data[:,0:numFeatures-1]
		yTest = data[:,numFeatures-1]

    #calling different classification methods
	runSVMTest(XTrain,yTrain,gtDataTrain,XTest,yTest,gtDataTest)
	runRFTest(XTrain,yTrain,gtDataTrain,XTest,yTest,gtDataTest)
	runDTTest(XTrain,yTrain,gtDataTrain,XTest,yTest,gtDataTest)
	runLinRegTest(XTrain,yTrain,gtDataTrain,XTest,yTest,gtDataTest)
	runLogRegTest(XTrain,yTrain,gtDataTrain,XTest,yTest,gtDataTest)


#running cross validation
def runClassification():
	print "\n*** Running cross validation ***"
	with open('gtDataTrain.txt', 'r') as f:
		gtData = json.loads(f.read())

	with open('featureDataTrain.txt', 'r') as f:
		allFeatureList = json.loads(f.read())
		numInstances = len(allFeatureList)
		numFeatures = len(allFeatureList[0])
		print "Number of training instances: ", numInstances, "Number of features: ", numFeatures
		data = np.array(allFeatureList)
		X = data[:,0:numFeatures-1]
		y = data[:,numFeatures-1]

	runSVM(X,y,gtData)
	runRandomForest(X,y, gtData)
	runDecisionTree(X,y,gtData)
	runLinearReg(X,y,gtData)
	runLogisticReg(X,y,gtData)

def main(argv):
	if len(argv)==2:
		if argv[1] == "train":	
			runClassification()
		else:
			if argv[1] == "test":		
				runTestClassification()
	else:
		runClassification()
		runTestClassification()

if __name__ == "__main__":
    main(sys.argv)