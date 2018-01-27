#coding: utf-8

import numpy as np

def loadExData():
	return [[1, 1, 1, 0, 0],
			[2, 2, 2, 0, 0],
			[1, 1, 1, 0, 0],
			[5, 5, 5, 0, 0],
			[1, 1, 0, 2, 2],
			[0, 0, 0, 3, 3],
			[0, 0, 0, 1, 1]]

def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

#下面的三个函数分别是几种不同的距离计算公式
def ecludSim(inA, inB):
	return 1.0 / (1.0 + np.linalg.norm(inA - inB))

def pearsSim(inA, inB):
	if len(inA) < 3:
		return 1.0
	return 0.5 + 0.5 * np.corrcoef(inA, inB, rowvar=0)[0][1]

def cosSim(inA, inB):
	num = float(inA.T * inB)
	denom = np.linalg.norm(inA) * np.linalg.norm(inB)
	return 0.5 + 0.5 * (num / denom)

#用来计算在给定相似度计算方法的条件下，用户对物品的估计评分值
#输入参数为：数据矩阵，用户编号，物品编号，相似度计算方法
#数据矩阵行为用户编号，列为物品编号
def standEst(dataMat, user, simMeas, item):
	n = np.shape(dataMat)[1]
	simTotal = 0.0; ratSimTotal = 0.0;
	for j in range(n):
		userRating = dataMat[user, j]
		if userRating == 0:
			continue
		#寻找两个用户都评分的物品
		overLap = np.nonzero(np.logical_and(dataMat[:, item].A > 0, dataMat[:, j].A > 0))[0]
		if len(overLap) == 0:
			similarity = 0
		else:
			similarity = simMeas(dataMat[overLap, item], dataMat[overLap, j])
		#print 'the %d and %d similarity is: %f' % (item, j, similarity)
		simTotal += similarity
		ratSimTotal += similarity * userRating
	if simTotal == 0:
		return 0
	else:
		return ratSimTotal / simTotal

#推荐算法，调用standEst算法
#产生最高的N个推荐结果
def recommend(dataMat, user, N=3, simMeas=cosSim, estMethod=standEst):
	unratedItems = np.nonzero(dataMat[user, :].A == 0)[1]
	if len(unratedItems) == 0:
		return 'you rated everything'
	itemScores = []
	for item in unratedItems:
		estimatedScore = estMethod(dataMat, user, simMeas, item)
		itemScores.append((item, estimatedScore))
	return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]

#基于SVD的评分估计
def svdEst(dataMat, user, simMeas, item):
	n = np.shape(dataMat)[1]
	simTotal = 0.0; ratSimTotal = 0.0;
	U, Sigma, VT = np.linalg.svd(dataMat)
	Sig4 = np.mat(np.eye(4) * Sigma[:4]) #建立对角矩阵
	xformedItems = dataMat.T * U[:, :4] * Sig4.I  #构建转换后的物品
	for j in range(n):
		userRating = dataMat[user, j]
		if userRating == 0 or j == item:
			continue
		similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)
		print 'the %d and %d similarity is : %f' % (item, j, similarity)
		simTotal += similarity
		ratSimTotal += similarity * userRating
	if simTotal == 0:
		return 0
	else:
		return ratSimTotal / simTotal

def printMat(inMat, thresh=0.8):
	for i in range(32):
		for k in range(32):
			if float(inMat[i, k] > thresh):
				print 1,
			else:
				print 0,
		print ' '

def imgCompress(numSV=3, thresh=0.8):
	myl = []
	for line in open('0_5.txt', 'r').readlines():
		newRow = []
		for i in range(32):
			newRow.append(int(line[i]))
		myl.append(newRow)
	myMat = np.mat(myl)
	print '****origin matrix*****'
	printMat(myMat, thresh)
	U, Sigma, VT = np.linalg.svd(myMat)
	SigRecon = np.mat(np.zeros((numSV, numSV)))
	for k in range(numSV):
		SigRecon[k, k] = Sigma[k]
	reconMat = U[:, :numSV] * SigRecon * VT[:numSV, :]
	print '****reconstructed matrix using %d singular values******' % numSV
	printMat(reconMat, thresh)