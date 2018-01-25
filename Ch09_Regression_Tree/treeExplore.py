#coding: utf-8

from numpy import *

from Tkinter import *
import regTrees

import matplotlib

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS, tolN):
	reDraw.f.clf()
	reDraw.a = reDraw.f.add_subplot(111)
	#检查复选框是否选中
	if chkBtnVar.get():
		if tolN < 2:
			tolN = 2
		myTree = regTrees.createTree(reDraw.rawDat, regTrees.modelLeaf, regTrees.modelErr, (tolS, tolN))
		yHat = regTrees.createForeCast(myTree, reDraw.testDat, regTrees.modelTreeEval)
	else:
		myTree = regTrees.createTree(reDraw.rawDat, ops=(tolS, tolN))
		yHat = regTrees.createForeCast(myTree, reDraw.testDat)
	#print shape(reDraw.rawDat[:,0])
	reDraw.a.scatter(reDraw.rawDat[:,0].flatten().A[0], reDraw.rawDat[:,1].flatten().A[0], s=5)
	reDraw.a.plot(reDraw.testDat, yHat, linewidth=2.0)
	reDraw.canvas.show()

def getInputs():
	try:
		tolN = int(tolNentry.get())
	except:
		#清除错误的输入并用默认值替换
		tolN = 10
		print 'entry Integer for tolN'
		tolNentry.delete(0, END)
		tolNentry.insert(0, '10')
	try:
		tolS = float(tolSentry.get())
	except Exception as e:
		#raise e
		tolS = 1.0
		print 'enter Float for tolS'
		tolSentry.delete(0, END)
		tolSentry.insert(0, '1.0')
	return tolN, tolS

#调用getInputs()方法得到输入框的值，利用该值调用reDraw()方法生成漂亮的图
def drawNewTree():
	tolN, tolS = getInputs()
	reDraw(tolS, tolN)

root = Tk()

#Label(root, text='Plot Place Holder').grid(row=0, columnspan=3)
reDraw.f = Figure(figsize=(5,4), dpi=100)
reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0, columnspan=3)

Label(root, text='tolN').grid(row=1, column=0)
tolNentry = Entry(root) #文本输入框
tolNentry.grid(row=1, column=1)
tolNentry.insert(0, '10')
Label(root, text='tolS').grid(row=2, column=0)
tolSentry = Entry(root)
tolSentry.grid(row=2, column=1)
tolSentry.insert(0, '1.0')
Button(root, text='ReDraw', command=drawNewTree).grid(row=1, column=2, rowspan=3)

#Button(root, text='Quit', fg='black', command=root.quit).grid(row=1, column=2)

chkBtnVar = IntVar()  #按键整数值
chkBtn = Checkbutton(root, text='Model Tree', variable=chkBtnVar) #复选按钮
chkBtn.grid(row=3, column=0, columnspan=2)

#初始化与reDraw关联的全局变量
reDraw.rawDat = mat(regTrees.loadDataSet('sine.txt'))
reDraw.testDat = arange(min(reDraw.rawDat[:,0]), max(reDraw.rawDat[:,0]), 0.01)

reDraw(1.0, 10)
root.mainloop()