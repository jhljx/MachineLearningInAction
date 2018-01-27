# coding: utf-8

from numpy import *

def loadSimpleData():
	datMat = np.matrix([[1.,2.1],
		[2.,1.1],
		[1.3,1.],
		[1.,1.],
		[2.,1.]])
	classLabels = [1.0,1.0,-1.0,-1.0,1.0]
	return datMat,classLabels

#第一个函数用于测试是否有某个值小于或大于我们正在测试的阈值。
def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
	retArray = ones((shape(dataMatrix)[0],1))  #生成二维数组，有shape(dataMatrix)[0]个元素，每个元素为一个list,有一个元素
	if threshIneq == 'lt':
		retArray[dataMatrix[:,dimen] <= threshVal] = -1.0
	else:
		retArray[dataMatrix[:,dimen] > threshVal] -1.0
	return retArray

#第二个函数用于在一个加权数据集中循环，并找到具有最低错误率的单层决策树
#返回值除了具有最小错误率的单层决策树，还有最小错误率及估计的类别向量
def buildStump(dataArr, classLabels, D):
	dataMatrix = mat(dataArr); labelMat = mat(classLabels).T
	m, n = shape(dataMatrix)
	numSteps = 10.0; bestStump = {}; bestClasEst = mat(zeros((m,1)))
	#bestStump村粗给定权重向量D时所得到的最佳单层决策树的相关信息
	#numSteps用于在特征的所有可能值上进行遍历
	minError = inf
	#minError用于寻找最小的错误率
	for i in range(n):
		rangeMin = dataMatrix[:,i].min(); rangeMax = dataMatrix[:,i].max();
		stepSize = (rangeMax - rangeMin)/numSteps
		#设置步长，其实将阈值设置在范围之外也行
		for j in range(-1, int(numSteps)+1):
			for inequal in ['lt', 'gt']:
				threshVal = (rangeMin + float(j)*stepSize)
				predictedVals = stumpClassify(dataMatrix, i, threshVal, inequal)
				errArr = mat(ones((m,1)))
				errArr[predictedVals == labelMat] = 0
				#这里我们基于权重向量D而不是其他错误计算指标来评价分类器
				weightedError = D.T*errArr
				#print "split:dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (i, threshVal, inequal, weightedError)
				if weightedError < minError:
					minError = weightedError
					bestClasEst = predictedVals.copy()
					bestStump['dim'] = i
					bestStump['thresh'] = threshVal
					bestStump['ineq'] = inequal
	return bestStump, minError, bestClasEst

#算法输入包括数据集、类标签、迭代次数numIt
#DS表示单层决策树(decision stump)
def adaBoostTrainDS(dataArr, classLabels, numIt = 40):
	weakClassArr = []
	m = shape(dataArr)[0]
	D = mat(ones((m,1))/m) #权重向量
	#记录每个数据点的类别估计累加值
	aggClassEst = mat(zeros((m,1)))
	for i in range(numIt):
		bestStump, error, classEst = buildStump(dataArr, classLabels, D)
		#print "D: ", D.T
		alpha = float(0.5*log((1.0 - error)/max(error, 1e-16)))  #保证除法不会出现除零溢出
		bestStump['alpha'] = alpha
		weakClassArr.append(bestStump)
		#print "classEst: ", classEst.T
		#为下一次迭代计算D
		expon = multiply(-1*alpha*mat(classLabels).T, classEst)
		D = multiply(D, exp(expon))
		D = D/D.sum()
		#错误率累加计算
		aggClassEst += alpha * classEst
		#print "aggClassEst：", aggClassEst.T
		aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))
		errorRate = aggErrors.sum() / m
		print "total error: ", errorRate
		if(errorRate == 0.0): break
	return weakClassArr, aggClassEst

#利用训练出的多个弱分类器进行分类的函数
def adaClassify(datToClass, classifierArr):
	dataMatrix = mat(datToClass)
	m = shape(dataMatrix)[0]
	aggClassEst = mat(zeros((m, 1)))
	for i in range(len(classifierArr)):
		classEst  = stumpClassify(dataMatrix, classifierArr[i]['dim'], classifierArr[i]['thresh'], classifierArr[i]['ineq'])
		aggClassEst += classifierArr[i]['alpha'] * classEst
		#print aggClassEst
	return sign(aggClassEst)


def loadDataSet(fileName):
	numFeat = len(open(fileName).readline().split('\t'))
	dataMat = []
	labelMat = []
	fr = open(fileName)
	for line in fr.readlines():
		lineArr = []
		curLine = line.strip().split('\t')
		for i in range(numFeat - 1):
			lineArr.append(float(curLine[i]))
		dataMat.append(lineArr)
		labelMat.append(float(curLine[-1]))
	return dataMat, labelMat

def plotROC(predStrengths, classLabels):
	import matplotlib.pyplot as plt
	cur = (1.0, 1.0)
	ySum = 0.0
	numPosClas = sum(array(classLabels)==1.0)
	yStep = 1 / float(numPosClas)
	xStep = 1 / float(len(classLabels) - numPosClas)
	#获得排序好的索引
	sortedIndices = predStrengths.argsort()
	fig = plt.figure()
	fig.clf()
	ax = plt.subplot(111)
	for index in sortedIndices.tolist()[0]:
		if classLabels[index] == 1.0:
			delX = 0; delY = yStep;
		else:
			delX = xStep; delY = 0;
			ySum += cur[1]
		ax.plot([cur[0], cur[0] - delX], [cur[1], cur[1] - delY], c='b')
		cur = (cur[0] - delX, cur[1] - delY)
	ax.plot([0, 1], [0, 1], 'b--')
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('ROC curve for AdaBoost Horse Colic Detection System')
	ax.axis([0, 1, 0, 1])
	plt.show()
	print 'the Area under the Curve is: ', ySum * xStep
