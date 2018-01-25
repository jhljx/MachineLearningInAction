#coding: utf-8

from numpy import *
import matplotlib.pyplot as plt

def loadDataSet(fileName):
	dataMat = []
	fr = open(fileName)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		fltLine = map(float, curLine)
		dataMat.append(fltLine)
	return dataMat


def distEclud(vecA, vecB):
	return sqrt(sum(power(vecA - vecB, 2)))

#生成k个随机的质心
def randCent(dataSet, k):
	n = shape(dataSet)[1]
	centroids = mat(zeros((k,n)))
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j]) - minJ)
		centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
	return centroids


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent, figureOn=True):
	m = shape(dataSet)[0]
	print "m = " + str(m)
	clusterAssment = mat(zeros((m,2)))
	centroids = createCent(dataSet, k)
	clusterChanged = True
	numIt = 0
	while(clusterChanged):
		numIt += 1
		clusterChanged = False
		for i in range(m):
			minDist = inf
			minIndex = -1
			for j in range(k):
				distJI = distMeas(centroids[j,:], dataSet[i,:])
				if distJI < minDist:
					minDist = distJI
					minIndex = j
			if clusterAssment[i, 0] != minIndex:
				clusterChanged = True
			clusterAssment[i, :] = minIndex, minDist**2
		if(figureOn):
			fig = plt.figure()
			ax = fig.add_subplot(111)
		for cent in range(k):
			pstInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
			#if(len(pstInClust) == 0):  #有时候会出现pstInClust为[]的情况
				#continue
			centroids[cent, :] = mean(pstInClust, axis=0)  #按列方向进行计算
			if(figureOn):
				ax.scatter(pstInClust[:,0].flatten().A[0], pstInClust[:,1].flatten().A[0])
		if(figureOn):
			ax.plot(centroids[:,0].flatten().A[0], centroids[:,1].flatten().A[0], 'r+', markerSize=10)
			plt.show()
		print centroids
	print "numIt = " + str(numIt)
	return centroids, clusterAssment



def biKmeans(dataSet, k, distMeas=distEclud):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m, 2)))  #初始所有点的簇编号均为0
	centroid0 = mean(dataSet, axis=0).tolist()[0]
	centList = [centroid0]
	print "centList:", centList
	for j in range(m):
		clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2
	while (len(centList) < k):
		print "-------------------"
		lowestSSE = inf
		for i in range(len(centList)):
			pstInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0], :]
			centroidMat, splitClustAss = kMeans(pstInCurrCluster, 2, distMeas, figureOn=False)
			sseSplit = sum(splitClustAss[:, 1])
			sseNoSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])
			print "sseSplit, and notSplit: ", sseSplit, sseNoSplit
			if (sseSplit + sseNoSplit) < lowestSSE:
				bestCentToSplit = i
				bestNewCents = centroidMat
				bestClustAss = splitClustAss.copy()
				lowestSSE = sseSplit + sseNoSplit
		#bestClustAss中只有属于最优的那个类划分后的结果
		#下面两个是数组过滤器，划分后生成了0,1的两个簇
		bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0], 0] = len(centList)
		bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0], 0] = bestCentToSplit
		print "the bestCentToSplit is: ", bestCentToSplit
		print "the len of bestClustAss is: ", len(bestClustAss)
		centList[bestCentToSplit] = bestNewCents[0, :]
		centList.append(bestNewCents[1,:])
		#更新最终的clusterAssment
		clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] = bestClustAss
		print centList
	fig = plt.figure()
	ax = fig.add_subplot(111)
	for cent in range(k):
		pstInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
		ax.scatter(pstInClust[:,0].flatten().A[0], pstInClust[:,1].flatten().A[0])
		ax.plot(centList[cent][:, 0].flatten().A[0], centList[cent][:, 1].flatten().A[0], 'r+', markerSize=10)
	plt.show()
	return centList, clusterAssment


