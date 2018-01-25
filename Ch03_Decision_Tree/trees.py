# coding: utf-8

from math import log
import operator

def createDataSet():
	dataSet = [[1, 1, 'yes'],
			[1, 1, 'yes'],
			[1, 0, 'no'],
			[0, 1, 'no'],
			[0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	return dataSet, labels


# 计算给定数据集的香农熵
def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCounts = {}
	#为所有可能分类创建字典
	for featVec in dataSet:
		currentLabel = featVec[-1]  # 
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	# print labelCounts
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key]) / numEntries
		#以2为底求对数
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt

#按照给定特征划分数据集
#三个参数：待划分的数据集，划分数据集的特征，需要返回的特征的值
def splitDataSet(dataSet, axis, value):
	#创建新的list对象
	retDataSet = []
	#抽取
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

#选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1
	#print(numFeatures)
	#计算整个数据集的原始香农熵，保存最初的无序度量值，用于与划分之后的数据集计算的熵进行比较
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet) / float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if(infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature


#计算该类被划分的分类名称
def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]

#创建决策树
#使用了两个变量: 数据集和标签列表
def createTree(dataSet, labels):
 	classList = [examle[-1] for examle in dataSet]  #包含了数据集中的所有类标签
 	#类别完全相同则停止继续划分
 	if classList.count(classList[0]) == len(classList):
 		return classList[0]
 	#遍历完所有特征时返回出现次数最多的（使用完了所有特征，但是仍然无法将数据集划分成仅包含唯一类别的分组）
 	if len(dataSet[0]) == 1:
 		return majorityCnt(classList)
 	bestFeat = chooseBestFeatureToSplit(dataSet)
 	bestFeatLabel =	labels[bestFeat]
 	myTree = {bestFeatLabel:{}}
 	del(labels[bestFeat])
 	featValues = [examle[bestFeat] for examle in dataSet]
 	uniqueVals = set(featValues)
 	for value in uniqueVals:
 		subLabels = labels[:]  #复制类标签，原因是python函数参数传递为引用传递，为了不改变原始列表的内容
 		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value), subLabels)
 	return myTree


#使用决策树的分类函数
def classify(inputTree, featLabels, testVec):
	firstStr = inputTree.keys()[0]
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)   #将标签字符串转换成索引
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key], featLabels, testVec)
			else:
				classLabel = secondDict[key]
	return classLabel

#使用pickle模块存储决策树
def storeTree(inputTree, filename):
	import pickle
	fw = open(filename, 'w')
	pickle.dump(inputTree, fw)


#从磁盘读取决策树文件
def grabTree(filename):
	import pickle
	fr = open(filename)
	return pickle.load(fr)



