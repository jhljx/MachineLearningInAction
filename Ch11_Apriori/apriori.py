#coding: utf-8

def loadDataSet():
	#return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
	return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [1, 2, 3, 4, 5], [1, 3, 4, 5], [1, 2, 3, 5, 6], [1, 2, 3, 5, 7], [1, 2, 3, 5, 8], \
	[1, 2, 3, 5, 9], [2, 3, 5, 6], [2, 4, 5], [2, 5]]

def createC1(dataSet):
	C1 = [] #C1是大小为1的所有候选项集的集合
	for transaction in dataSet:
		for item in transaction:
			if not [item] in C1:
				C1.append([item])
	C1.sort()
	return map(frozenset, C1)

#Apriori算法首先构建集合C1,然后扫描数据集来判断这些只有一个元素的项集是否满足最小支持度的要求。
#满足最小支持度要求的项集构成集合L1。L1中的元素相互组合构成C2，C2再进一步过滤变成L2。
def scanD(D, Ck, minSupport):
	ssCnt = {}
	for tid in D:
		for can in Ck:
			if can.issubset(tid):
				if can not in ssCnt:
					ssCnt[can] = 1
				else:
					ssCnt[can] += 1
	numItems = float(len(D))
	retList = []
	supportData = {}
	for key in ssCnt:
		support = ssCnt[key] / numItems
		if support >= minSupport:
			retList.insert(0, key)
		supportData[key] = support
	return retList, supportData

#创建候选项集
def aprioriGen(Lk, k): #creates Ck
	retList = []
	lenLk = len(Lk) #len为k-1，所以比较两个set的k-2个数是否相同，进而构造长度为k的set
	for i in range(lenLk):
		for j in range(i + 1, lenLk):
			L1 = list(Lk[i])[:k-2]
			L2 = list(Lk[j])[:k-2]
			L1.sort()
			L2.sort()
			if L1 == L2:
				retList.append(Lk[i] | Lk[j])
	return retList


def apriori(dataSet, minSupport=0.5):
	C1 = createC1(dataSet)
	D = map(set, dataSet)
	L1, supportData = scanD(D, C1, minSupport)
	L = [L1]
	k = 2
	while(len(L[k - 2]) > 0):
		Ck = aprioriGen(L[k - 2], k)
		Lk, supK = scanD(D, Ck, minSupport)
		supportData.update(supK)
		L.append(Lk)
		k += 1
	return L, supportData

#三个参数：频繁项集列表，包含那些频繁项集支持数据的字典，最小可信度阈值
def generateRules(L, supportData, minConf=0.7):
	bigRuleList = []
	#从频繁项集的元素个数为2开始遍历(L[1]的频繁项集元素为2，无法从单个元素项集中构建关联规则)
	for i in range(1, len(L)):
		for freqSet in L[i]:
			H1 = [frozenset([item]) for item in freqSet]
			if(i > 1): #频繁项集的元素数目超过2，i=2时频繁项集元素数目为3
				rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
			else:
				calcConf(freqSet, H1, supportData, bigRuleList, minConf)
	return bigRuleList


def calcConf(freqSet, H, supportData, brl, minConf=0.7):
	prunedH = []
	for conseq in H:
		#可信度计算直接使用supportData中的数值，可以节省大量时间
		conf = supportData[freqSet] / supportData[freqSet - conseq]
		if(conf >= minConf):
			print freqSet-conseq, '-->', conseq, 'conf:', conf
			brl.append((freqSet-conseq, conseq, conf))
			prunedH.append(conseq)
	return prunedH


def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
	m = len(H[0])  #H中频繁项集的大小
	if(len(freqSet) > (m + 1)):
		Hmp1 = aprioriGen(H, m + 1)
		Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
		if(len(Hmp1) > 1):
			rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)