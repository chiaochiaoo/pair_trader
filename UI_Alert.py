import matplotlib.pyplot as plt 
from matplotlib.widgets import TextBox
import threading
import time
import matplotlib as mpl


def appendText(ax,h,text,box,break3):
	lst = []
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

class UI_Alert():


	def __init__(self):
		mpl.rcParams['toolbar'] = 'None' 
		self.fig = plt.figure(figsize=(5,5))
		self.fig.canvas.set_window_title('ALERT WINDOW')
		self.bbox = {'facecolor': 'white', 'alpha': 0.5, 'pad': 3}
		self.ax = plt.axes([0, 0, 1, 1])
		self.init = TextBox(self.ax, 'GRAPH CMDs:', initial="")
		self.text1 = ["vol1:      ","range1:  ","roc1:      ","vol5:       ","range5:  ","roc5:       ","vol30:      ","range30: ","roc30:      "]
		self.text2 = ["PastOneMonth: ","PastOneWeek: ","PastOneDay: ","Current:      ","Vol ratio1: ","Tran ratio1 ","Correlation 1 "]
		self.sval = [0,0,0,0,0,0,0,0,0,0]
		self.qval= [0,0,0,0,0,0,0,0,0,0]

		self.stext = appendText(self.ax,0.1,self.text1,self.bbox,True)
		self.qtext = appendText(self.ax,0.3,self.text1,self.bbox,True)
		self.pairtext = appendText(self.ax,0.55,self.text2,self.bbox,False)

	def redraw(self):
		plt.draw()




	# for j in range(4):

	# 	for i in range(len(text)):
	# 		offset = 0
	# 		if i>2:
	# 			offset =0.02
	# 		if i >5:
	# 			offset =0.04
	# 		display(ax, 0.05+0.1*j, 0.5-(((i+1)/24)+offset), text[i], 0, 0, l)
			

	# for i in range(len(text2)):
	# 	display(ax, 0.45, 0.5-(((i+1)/24)), text2[i], 0, 0, 0)


ui = UI_Alert()

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