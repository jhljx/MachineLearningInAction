#coding: utf-8

class treeNode:
	def __init__(self, nameValue, numOccur, parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None
		self.parent = parentNode
		self.children = {}

	def inc(self, numOccur):
		self.count += numOccur

	def disp(self, ind=1):
		print '	'*ind, self.name, '	', self.count
		for child in self.children.values():
			child.disp(ind+1)


def createTree(dataSet, minSup=1):
	headerTable = {}
	for trans in dataSet:
		for item in trans:
			headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

	#移除不满足最小支持度的元素项
	for k in headerTable.keys():
		if headerTable[k] < minSup:
			del(headerTable[k])

	print 'headerTable: ', headerTable
	freqItemSet = set(headerTable.keys())
	#print 'freqItemSet: ', freqItemSet
	#如果没有元素项满足要求，则退出
	if len(freqItemSet) == 0:
		return None, None
	for k in headerTable:
		headerTable[k] = [headerTable[k], None]
	retTree = treeNode('NULL Set', 1, None)
	for tranSet, count in dataSet.items():
		localD = {}
		#根据全局频率对每个事务中的元素进行排序
		for item in tranSet:
			if item in freqItemSet:
				localD[item] = headerTable[item][0]
		if len(localD) > 0:
			#使用排序后的频繁项集对树进行填充
			orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p:p[1], reverse=True)]
			updateTree(orderedItems, retTree, headerTable, count)
	return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
	if items[0] in inTree.children:
		inTree.children[items[0]].inc(count)
	else:
		inTree.children[items[0]] = treeNode(items[0], count, inTree)
		if headerTable[items[0]][1] == None:
			headerTable[items[0]][1] = inTree.children[items[0]]
		else:
			updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
	if(len(items) > 1):
		updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
	while(nodeToTest.nodeLink != None):
		nodeToTest = nodeToTest.nodeLink
	nodeToTest.nodeLink = targetNode

def loadSimpDat():
	simpDat = [['r', 'z', 'h', 'j', 'p'],
	           ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
	           ['z'],
	           ['r', 'x', 'n', 'o', 's'], 
	           ['y', 'r', 'x', 'z', 'q', 't', 'p'],
	           ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
	return simpDat

def createInitSet(dataSet):
	retDict = {}
	for trans in dataSet:
		retDict[frozenset(trans)] = 1
	return retDict


def ascendTree(leafNode, prefixPath):
	if leafNode.parent != None:
		ascendTree(leafNode.parent, prefixPath)
		prefixPath.append(leafNode.name)

def findPrefixPath(basePat, treeNode):
	condPats = {}
	while treeNode != None:
		prefixPath = []
		ascendTree(treeNode, prefixPath)
		if len(prefixPath) > 1:
			condPats[tuple(prefixPath[:-1])] = treeNode.count
		treeNode = treeNode.nodeLink
	return condPats

#这个函数写的并不好，递归的重复节点太多了，mmp
def mineTree(inTree, headerTable, minSup, preFix, freqItemList, level=1):
	bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
	print 'bigL: ', bigL, '; level: ', level
	#return
	#从头指针表的底端开始

	for basePat in bigL:
		print 'basePat: ', basePat, '; level: ', level
		newFreqSet = preFix.copy()
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
		print 'condPattBases: ', condPattBases
		#从条件模式基来构建条件FP树
		myCondTree, myHead = createTree(condPattBases, minSup)
		if myHead != None:  # 挖掘条件FP树
			print 'conditional tree for: ', newFreqSet
			myCondTree.disp()
			mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList, level+1)