#coding: utf-8

import numpy as np
import random

#创建实验样本
def loadDataSet():
	postingList = [['my', 'dog', 'has', 'flea', \
					'problems', 'help', 'please'],
				   ['maybe', 'not', 'take', 'him', \
					'to', 'dog', 'park', 'stupid'],
				   ['my', 'dalmation', 'is', 'so', 'cute', \
				    'I', 'love', 'him'],
				   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
				   ['mr', 'licks', 'ate', 'my', 'steak', 'how', \
				    'to', 'stop', 'him'],
				   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
	classVec = [0, 1, 0, 1, 0, 1]  # 1表示侮辱性的文字 0表示正常言论
	return postingList, classVec


#创建包含在所有文档中出现的不重复的单词列表
def createVocabList(dataSet):
	vocabSet = set([])
	#创建两个集合的并集
	for document in dataSet:
		vocabSet = vocabSet | set(document)
	return list(vocabSet)

#inputSet是word的一个vector
def setOfWords2Vec(vocabList, inputSet):
	#创建一个其中所含元素都为0的向量
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word: %s is not in my Vocabulary!" % word
	return returnVec


#与setOfWords2Vec词集模型对比，该方法为词袋模型
def bagOfWords2VecMN(vocabList, inputSet):
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
	return returnVec


#trainMat是单词是否在vocabulary中的01 Mat数组
#trainCategory的维度和trainMat的第一维相同，表示每一组数据的类别，是否为侮辱性语句，01数组
def trainNB0_Old(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = np.sum(trainCategory) / float(numTrainDocs)
	p0Num = np.zeros(numWords)
	p1Num = np.zeros(numWords)
	p0Denom = 0.0
	p1Denom = 0.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += np.sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += np.sum(trainMatrix[i])
	p1Vect = p1Num / p1Denom    # change to log()
	p0Vect = p0Num / p0Denom    # change to log()
	return p0Vect, p1Vect, pAbusive


#输入的trainMatrix和trainCategory都是numpy的array
def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	pAbusive = np.sum(trainCategory) / float(numTrainDocs)
	#初始化概率
	p0Num = np.ones(numWords)
	p1Num = np.ones(numWords)
	p0Denom = 2.0
	p1Denom = 2.0
	#向量相加
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += np.sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += np.sum(trainMatrix[i])
	#每个元素除以该类别的总词数
	p1Vect = np.log(p1Num / p1Denom)    # change to log()
	p0Vect = np.log(p0Num / p0Denom)    # change to log()
	return p0Vect, p1Vect, pAbusive

#参数为要分类的向量vec2Classify,使用trainNB0得到的三个概率
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
	p1 = np.sum(vec2Classify * p1Vec) + np.log(pClass1)
	p0 = np.sum(vec2Classify * p0Vec) + np.log(1.0 - pClass1)
	if(p1 > p0):
		return 1
	else:
		return 0


def testingNB():
	listOPosts, listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	p0V, p1V, pAb = trainNB0(np.array(trainMat), np.array(listClasses))
	testEntry = ['love', 'my', 'dalmation']
	thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
	testEntry = ['stupid', 'garbage']
	thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)


def textParse(bigString):
	#去掉少于两个的字符串，并将所有字符串转换为小写
	import re
	listOfTokens = re.split(r'\W*', bigString)
	return [token.lower() for token in listOfTokens if len(token) > 2]


def spamTest():
	docList, classList, fullText = [], [], []
	#导入并解析文件
	for i in range(1, 26):
		wordList = textParse(open('email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	trainingSet = range(50)
	testSet = []
	#随机构造训练集，构造完需要剔除，将随机选择出的10个加入测试集，用剩下的训练
	for i in range(10):
		randIndex = int(random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat, trainClasses = [], []
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V, p1V, pSpam = trainNB0(np.array(trainMat), np.array(trainClasses))
	#对测试集分类
	errorCount = 0
	#errorList = []
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList, docList[docIndex])
		if classifyNB(np.array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
			errorCount += 1
	#print errorList
	print 'the error rate is: ', float(errorCount) / len(testSet)

#计算出现频率
#遍历词汇表中的每个词并统计它在文本中出现的次数，然后根据出现次数从高到低对词典进行排序，返回排序最高的30个单词
def calcMostFreq(vocabList, fullText):
	import operator
	freqDict = {}
	for token in vocabList:
		freqDict[token] = fullText.count(token)
	sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedFreq[:30]


def localWords(feed1, feed0):
	import feedparser
	docList, classList, fullText = [], [], []
	minLen = min(len(feed1['entries']), len(feed0['entries']))
	#每次访问一条RSS源
	for i in range(minLen):
		wordList = textParse(feed1['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(feed0['entries'][i]['summary'])
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)
	vocabList = createVocabList(docList)
	top30Words = calcMostFreq(vocabList, fullText)
	#去掉出现次数最高的那些词
	for pairW in top30Words:
		if pairW[0] in vocabList:
			vocabList.remove(pairW[0])
	trainingSet = range(2 * minLen)
	testSet = []
	for i in range(20):
		randIndex = int(random.uniform(0, len(trainingSet)))
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	trainMat, trainClasses = [], []
	for docIndex in trainingSet:
		trainMat.append(bagOfWords2VecMN(vocabList, docList[docIndex]))
		trainClasses.append(classList[docIndex])
	p0V, p1V, pSpam = trainNB0(np.array(trainMat), np.array(trainClasses))
	errorCount = 0
	for docIndex in testSet:
		wordVector = bagOfWords2VecMN(vocabList, docList[docIndex])
		if classifyNB(np.array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
			errorCount += 1
	print 'the error rate is: ', float(errorCount) / len(testSet)
	return vocabList, p0V, p1V


def getTopWords(ny, sf):
	import operator
	vocabList, p0V, p1V = localWords(ny, sf)
	topNY, topSF = [], []
	for i in range(len(p0V)):
		if p0V[i] > -6.0:
			topSF.append((vocabList[i], p0V[i]))
		if(p1V[i] > -6.0):
			topNY.append((vocabList[i], p1V[i]))
	sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)
	print "SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**"
	for item in sortedSF:
		print item[0]
	sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
	print "NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**"
	for item in sortedNY:
		print item[1]








