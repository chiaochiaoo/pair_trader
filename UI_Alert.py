import matplotlib.pyplot as plt 
from matplotlib.widgets import TextBox
import threading
import time
import matplotlib as mpl
import pandas as pd
import numpy as np


def appendText(ax,h,text,box,break3,info):
	lst = []

	ax.text(h, 0.8, info)

	if break3:
		for i in range(len(text)):
			offset = 0
			if i>2:
				offset =0.02
			if i >5:
				offset =0.04
			lst.append(ax.text(h, 0.8-((i+1)/20)-offset, text[i]+str(0),bbox=box))
	else:
		for i in range(len(text)):
			lst.append(ax.text(h, 0.8-((i+1)/15), text[i]+str(0),bbox=box))
	return lst

def set_hist_vals(S):

	dic = {}

	avg = []
	std = []

	start=S[S['time']=='09:30'].index.values[0]
	end=S[S['time']=='16:00'].index.values[0]+1

	avg.append(np.mean(S["v1m"][start:end]))
	avg.append(np.mean(S["v5m"][start:end]))
	avg.append(np.mean(S["v30m"][start:end]))
	avg.append(np.mean(S["rm"][start:end]))
	avg.append(np.mean(S["r5m"][start:end]))
	avg.append(np.mean(S["r30m"][start:end]))
	avg.append(np.mean(S["rocm"][start:end]))
	avg.append(np.mean(S["roc5m"][start:end]))
	avg.append(np.mean(S["roc30m"][start:end]))

	std.append(np.std(S["v1m"][start:end]))
	std.append(np.std(S["v5m"][start:end]))
	std.append(np.std(S["v30m"][start:end]))

	std.append(np.std(S["rm"][start:end]))
	std.append(np.std(S["r5m"][start:end]))
	std.append(np.std(S["r30m"][start:end]))

	std.append(np.std(S["rocm"][start:end]))
	std.append(np.std(S["roc5m"][start:end]))
	std.append(np.std(S["roc30m"][start:end]))

	avg = [round(i,3) for i in avg]
	std = [round(i,3) for i in std]

	return avg,std

class alert_data():
	def __init__(self,symbols,UI_Alert):
		self.symbols = symbols[:]
		self.val = {}
		for i in symbols:
			self.val[i] = []

		self.UI_Alert = UI_Alert

		# lst : [vol1,vol5,vol30,r,r5,r30,roc,roc5,roc30 ]
	def set_val(self,symbol,lst):

		if symbol not in self.symbols:
			print("DONT HAVE ",symbol)
		else:
			self.val[symbol] = lst[:]

	def update_UI(self):
		# while True:
		s1 = self.symbols[0]
		s2 = self.symbols[1]

		self.UI_Alert.redraw(self.val[s1],self.val[s2])


class alert_data_pair():
	def __init__(self):
		self.spread=0


class UI_Alert():

	def __init__(self):
		mpl.rcParams['toolbar'] = 'None' 
		self.fig = plt.figure(figsize=(10,15))
		self.fig.canvas.set_window_title('ALERT WINDOW')
		self.bbox = {'facecolor': 'white', 'alpha': 0.5, 'pad': 3}
		self.ax = plt.axes([0.5, 0, 0.5,0.5])
		#self.init = TextBox(self.ax, 'GRAPH CMDs:', initial="")
		self.ax.axis("off")
		self.text1 = ["vol1:      ","vol5:       ","vol30:      ","range1:  ","range5:  ","range30: ","roc1:      ","roc5:       ","roc30:      "]
		self.text2 = ["PastOneMonth: ","PastOneWeek: ","PastOneDay: ","Current:      ","Vol ratio1: ","Tran ratio1 ","Correlation 1 "]


		self.stext = appendText(self.ax,0.1,self.text1,self.bbox,True,"SPY")
		self.qtext = appendText(self.ax,0.3,self.text1,self.bbox,True,"QQQ")
		self.pairtext = appendText(self.ax,0.55,self.text2,self.bbox,False,"PAIR")

		
		S =pd.read_csv('data/SPYstat.csv')
		Q =pd.read_csv('data/QQQstat.csv')

		self.savg,self.sstd = set_hist_vals(S)
		self.qval,self.qstd = set_hist_vals(Q)

		# TWO LIST OF VALUES
	def redraw(self,s,q):
		#set_text
		self.stext[0].set_text(s[0])
		self.stext[1].set_text(s[1])
		self.stext[2].set_text(s[2])
		self.stext[3].set_text(s[3])
		self.stext[4].set_text(s[4])
		self.stext[5].set_text(s[5])
		self.stext[6].set_text(s[6])
		self.stext[7].set_text(s[7])
		self.stext[8].set_text(s[8])

		self.qtext[0].set_text(q[0])
		self.qtext[1].set_text(q[1])
		self.qtext[2].set_text(q[2])
		self.qtext[3].set_text(q[3])
		self.qtext[4].set_text(q[4])
		self.qtext[5].set_text(q[5])
		self.qtext[6].set_text(q[6])
		self.qtext[7].set_text(q[7])
		self.qtext[8].set_text(q[8])
		#self.stext[0].set_backgroundcolor("blue")
		self.fig.canvas.draw()


	def printout(self):
		print(self.hist_val[0])



def aaaaa(ad):
	o = 1
	while True:
		lst = np.array([1,2,3,4,5,6,7,8,9])
		o+=1
		ad.set_val("SPY",lst+o)
		ad.set_val("QQQ",lst)
		ad.update_UI()
		time.sleep(2)

ui = UI_Alert()

ad = alert_data(["SPY","QQQ"],ui)


# ad.set_val("SPY",[1,2,3,4,5,6,7,8,9])
# ad.set_val("QQQ",[4,2,3,4,5,6,7,8,9])
# ad.update_UI()


#ad.call()
plt.show()
# fig = plt.figure(figsize=(5,5))
# bbox = {'facecolor': 'white', 'alpha': 0.5, 'pad': 3}
# ax = plt.axes([0, 0, 1, 1])

# text_box4 = TextBox(ax, 'GRAPH CMDs:', initial="")

#text = ["vol1:","vol5:","vol30:","range1:","range5:","range30:","roc1:","roc5:","roc30:"]

#text  = ["vol1:      ","range1:  ","roc1:      ","vol5:       ","range5:  ","roc5:       ","vol30:      ","range30: ","roc30:      "]
#text = text[::-1]
#values = [0,0,0,0,0,0,0,0,0,0]

# l=0
# def test():
# 	global l
# 	global fig
# 	l+=1
# 	a1.set_text(str(l))
# 	plt.draw()


# def tryx():

# 	while True:
# 		print("set new")
# 		test()
# 		time.sleep(1)
# a1.set_backgroundcolor("blue")

# t1 = threading.Thread(target=tryx, daemon=True)

# def display(ax,h,v,text,mean,std,cur):

# 	display = ""+str(cur)
# 	if cur ==0:
# 		ax.text(h, v, text+str(0),
# 		        bbox=white)
# 	elif abs(cur-mean)>2*std:
# 		ax.text(h, v, text+display,
# 		        bbox=red)
# 	elif abs(cur-mean)>std:
# 		ax.text(h, v, text+display,
# 		        bbox=yellow)
# 	else:
# 		ax.text(h, v, text+display,
# 		        bbox=green)
# #, style='italic'
# offset = 0

# l=0
# def redraw():
# 	global l
# 	l+=1
# 	f
# 	for j in range(4):

# 		for i in range(len(text)):
# 			offset = 0
# 			if i>2:

# 				offset =0.02

# 			if i >5:
# 				offset =0.04
# 			display(ax, 0.05+0.1*j, 0.5-(((i+1)/24)+offset), text[i], 0, 0, l)
			

# 	for i in range(len(text2)):
# 		display(ax, 0.45, 0.5-(((i+1)/24)), text2[i], 0, 0, 0)
# 	#fig.canvas.draw()


# def plot(datax, datay, name):
#     x = datax
#     y = datay**2
#     plt.scatter(x, y, label=name)
#     plt.legend()
#     plt.show()


# if __name__ == "__main__":   
#     for i in range(2):
#         p = multiprocessing.Process(target=plot, args=(i, i, i))
#         p.start()
# # if True:
#     #input('Vlaue: ') # while commented plots are shown