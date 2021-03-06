# coding: utf-8

import matplotlib.pyplot as plt

from pylab import *  
mpl.rcParams['font.sans-serif'] = ['SimHei']

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plotNode(nodeTxt, centerPt, parentPt, nodeType):

	createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
		textcoords='axes fraction', va='center', ha='center', bbox=nodeType, arrowprops=arrow_args)  
	#那会把axes fraction写错成axe fraction了

def createPlotOrigin():
	fig = plt.figure(1, facecolor='white')
	fig.clf()
	print 'yes'
	createPlot.ax1 = plt.subplot(111, frameon=False)
	print 'create'
	plotNode(U'决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
	print 'create 1'
	plotNode(U'叶节点', (0.8, 0.1), (0.3, 0.8), leafNode)
	plt.show()


def getNumLeafs(myTree):
	numLeafs = 0
	firstStr = myTree.keys()[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict': #测试节点的数据类型是否为字典
			numLeafs += getNumLeafs(secondDict[key])
		else:
			numLeafs += 1
	return numLeafs


def getTreeDepth(myTree):
	maxDepth = 0
	firstStr = myTree.keys()[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = 1 + getTreeDepth(secondDict[key])
		else:
			thisDepth = 1
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth

#输出预先存储的树的信息，避免每次测试代码时都要从数据中创建树的麻烦
def retrieveTree(i):
	listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
		{'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}]
	return listOfTrees[i]

#在父子节点之间填充文本信息
def plotMidText(cntrPt, parentPt, txtString):
	xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
	yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
	#createPlot.ax1.text(xMid, yMid, txtString) #如果是这样子的话，则树的边上的数字都是竖直的
	createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)   #这样的话，树的边上的数字会旋转倾斜


def plotTree(myTree, parentPt, nodeTxt):
	#计算树的宽与高
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)

	firstStr = myTree.keys()[0]
	cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
	plotMidText(cntrPt, parentPt, nodeTxt)  #标记子节点的属性值
	#绘制子节点具有的特征值，或者沿此分支向下的数据实例必须具有的特征值。
	plotNode(firstStr, cntrPt, parentPt, decisionNode)
	secondDict = myTree[firstStr]
	plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  #减少y偏移
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			plotTree(secondDict[key], cntrPt, str(key))
		else:
			plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
			plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
	plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


def createPlot(inTree):
	fig = plt.figure(1, facecolor='white',figsize=(7,7), dpi=105)
	fig.clf()
	axprops = dict(xticks=[], yticks=[])
	createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
	#全局变量totalW存储树的宽度，totalD存储树的深度
	plotTree.totalW = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	#树的宽度用于计算放置判断节点的位置，主要的计算原则是将它放在所有叶子节点中间，而不仅仅是它子节点的中间。
	#下面的两个全局变量用来追踪已经绘制的节点位置，以及放置下一个节点的恰当位置。
	plotTree.xOff = -0.5/plotTree.totalW
	plotTree.yOff = 1.0
	plotTree(inTree, (0.5,1.0), '')
	plt.show()


