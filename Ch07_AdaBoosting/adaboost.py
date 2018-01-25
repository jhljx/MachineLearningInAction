# coding utf-8

def loadSimpleData():
	datMat = matrix([[1.,2.1],
		[2.,1.1],
		[1.3,1.],
		[1.,1.],
		[2.,1.]])
	classLabels = [1.0,1.0,-1.0,-1.0,1.0]
	return dataMat,classLabels

def adaBoostTrainDS(dataArr, classLabels, numIt = 40):
	weakClassArr = []
	m = shape(dataArr)[0]
	D = mat(ones((m,1))/m)
	aggClassEst = mat(zeros((m,1)))
	for i in range(numIt):
		bestStump, error, classEst = buildStump(dataArr, classLabels, D)
		print("D: ", D.T)
		alpha = float(0.5*log((1.0 - error)/max(error, 1e-16)))
		bestStump['alpha'] = alpha
		weakClassArr.append(bestStump)
		print("classEst: ", classEst.T)
		expon = multiply(-1*alpha*mat(classLabels).T, classEst)
		D = multiply(D, exp(expon))
		D = D/D.sum()
		aggErrors = multiply(sign(aggClassEst) != mat(classLabels).T, ones((m,1)))
		errorRate = aggErrors.sum()/m
		print("total error: ", errorRate, "\n")
		if(errorRate == 0.0): break
	return weakClassArr

