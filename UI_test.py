import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import pandas as pd
import matplotlib.ticker as mticker
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import Functions as chiao


####TEST 1. One thread, Multiple Figures with FuncAnimation###### 


#### SUCCESS!! ####

### WWWOOOWW!! ###
a = [1,2,3]
b= [2,1,3]
def report(spy,qqq,sma,std):

	n = round(((spy-qqq)-sma)/std,2)

	text = ""
	if n >=0:
		text = "+" + str(n) + "STD away from the mean"
	else:
		text = "-" + str(n) + "STD away from the mean"
		print("g")

	return text


def update(self):
	global a
	global b
	a.append(a[-1]+1)
	b.append(3)
	t1.clear()
	t1.plot(a,b)
	print(a)

def update2(self):

	t2.plot(a,b)

	

plt.style.use("seaborn-darkgrid")
f = plt.figure(1)
f.canvas.set_window_title('f1')
t1 = f.add_subplot(111)

f2 = plt.figure(2)
f2.canvas.set_window_title('f2')
t2 = f2.add_subplot(111)



ani = FuncAnimation(f,update,fargs=(),interval=1000)
ani2 = FuncAnimation(f2,update2,fargs=(),interval=1000)
plt.show()