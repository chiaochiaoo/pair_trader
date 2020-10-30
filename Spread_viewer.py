import threading
import time
import pandas as pd
import numpy as np
import datetime
import Functions as chiao
from Data_processor import Data_processor
import matplotlib as mpl
import sys
import os
import Spread_viewer_function as SVF
##########################################

#############################################
TESTMODE = False
REALMODE = True
mpl.rcParams['toolbar'] = 'None' 

# 1. QUESTION IS. HOW DO I FEED THOSE DATA FEED TO UI?

# 2. QUESTION IS. WHAT DA FUCK AM I CALCULATING 


class Pair_trading_processor(Data_processor):

	# Requires more - Spread, Vol Ratio, and ROC, and Cor. 
	def __init__(self,symbols,interval,tos_mode,readlock):
		super().__init__(symbols,interval,tos_mode,readlock)

		self.pairs = (symbols[0],symbols[1])

		self.spread =0
		self.spread5 =0
		self.spread15 = 0

		#this is for minutes. 
		self.intra_spread = []
		self.intra_spread_MA5 = []
		self.intra_spread_MA15 = []


		self.intra_spread_seconds = []

		self.roc_1 = 0
		self.roc_5 = 0
		self.roc_15 = 0

		self.roc_1_list=[]
		self.roc_5_list=[]
		self.roc_15_list=[]

		self.cors_5 = []
		self.cors_15 = []


		self.max_spread_bin_today = [0]
		# self.max_spread_bin_weekly = w_dis
		# self.max_spread_bin_montly = m_dis

		# self.max_spread_1 = roc1
		# self.max_spread_5 = roc5
		# self.max_spread_15 = roc15

		# self.vol_ratio_15 = []
		# self.vol_ratio_30 = []

		# self.tran_ratio_15 = []
		# self.tran_ratio_30 = []


		self.enable = False

		if len(symbols)!=2:
			print("Console (PT): Pair trade mode on but Symbol numbers are not 2.")

		if len(symbols)==2:
			print("Console (PT): Pair trade mode on, Symbols: ",str(self.symbols))	
			self.enable = True	


	def start(self):

		print("Console (PT): Thread created, ready to start")
		t1 = threading.Thread(target=self.start_function, daemon=True)
		t1.start()
		print("Console (PT): Thread running. Continue:")


	def fetch_missing_data(self):

		#Set init price.

		#minute price: 9:30 to now.

		#minutes : 9:30 to now. 

		#Nake sure they sync. 

		s = [i[:i.index(".")] for i in self.symbols]

		ts = []
		ps = []
		for i in s:
			timestamp,price = SVF.fetch_data_yahoo(i)
			ts.append(timestamp[:-2])
			ps.append(price[:-2])


		#MUST SYNC THE DATA.
		if len(ts[1]) > len(ts[0]):
			for i in range(len(ts[1])-len(ts[0])):
				ps[0].append(ps[0][-1])
			ts[0] = ts[1][:]
		else:
			for i in range(len(ts[0])-len(ts[1])):
				ps[1].append(ps[1][-1])
			ts[1] = ts[0][:]


		
		#Now let's set init.
		for i in range(len(self.symbols)):
			self.init_price[self.symbols[i]] = ps[i][0]

		#Spread.
		# print(ps[0])
		# print(ps[1])
		c1 = (np.array(ps[0])-ps[0][0])*100/ps[0][0]
		c2 = (np.array(ps[1])-ps[1][0])*100/ps[1][0]



		self.intra_spread = list(c1 - c2)

		self.intra_spread_MA5 = list(chiao.SMA(self.intra_spread, 5))
		self.intra_spread_MA15 = list(chiao.SMA(self.intra_spread, 15))
		self.cur_minute_list = ts[0][:]

		#Time 





		#CAlculate init Spread.

	def start_function(self):

		print("Console (PT): Pair trading moudule begins. ")
		super().tos_start()
		self.fetch_missing_data()

		interval = self.interval

		x = 12
		a = self.pairs[0]
		b = self.pairs[1]

		while True:

			current_time = time.time()

			self.aggregate_data()

			lag = (time.time() - current_time)
			sleep = self.interval
			if interval*1000-lag> 0 : sleep = (interval*1000-lag)/1000

			if x %12 ==0:
				print("\nConsole (PT): Processing for ",round(lag*1000,2),"ms , Sleep for",round(sleep,5),"s \n")
				print(round(self.cur_price[a],2),round(self.cur_percentage_change[a],2),"\n",\
				round(self.cur_price[b],2),round(self.cur_percentage_change[b],2),"\n",\
				round(self.spread,5),round(self.roc_1,5),round(self.roc_5,5),round(self.roc_15,5),\
				self.intra_spread[-15:],\
				self.cur_minute_list[-15:],"\n")

			###if pair trade mode is on, display the info###

			# UI_pairtrade.update(self, self.readlock)
			x +=1 



			time.sleep(sleep)


	def aggregate_data(self):

		super().aggregate_data()
		now = datetime.datetime.now()
		t = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))


		a = self.pairs[0]
		b = self.pairs[1]

		self.spread = self.cur_percentage_change[a] - self.cur_percentage_change[b]

		# self.spread_ma5 = (sum(self.intra_spread[-300:]) + self.spread)/(len(self.intra_spread[-300:])+1) 
		# self.spread_ma15 = (sum(self.intra_spread[-900:]) + self.spread)/(len(self.intra_spread[-900:])+1)

		#What if not that time yet. intra_spread_seconds


		if len(self.intra_spread_seconds)>0:
			len_ = min(60, len(self.intra_spread_seconds)-1)
			self.roc_1 = self.spread-self.intra_spread_seconds[-len_] 

		if len(self.intra_spread)>0:			
			len_ = min(5, len(self.intra_spread)-1)

			#print(len_,self.intra_spread[-len_],self.spread)
			self.roc_5 = self.spread- self.intra_spread_MA5[-len_] 

			len_ = min(15, len(self.intra_spread)-1)
			#print(len_,self.intra_spread[-len_],self.spread)
			self.roc_15 = self.spread-self.intra_spread_MA15[-len_] 



		# correlation.
		cor_5 = 0
		cor_15 = 0

		if  len(self.minute_open_list[a]) >= 4:
			# print("length:",len(self.cur_price_list[a]),len(self.cur_price_list[b]))
			# print("pass in :",self.cur_price_list[a][-120:],self.cur_price_list[b][-120:])
			# print("pass in :",self.cur_price_list[a][-120:][:-1],self.cur_price_list[b][-120:][:-1])
			cor_5 = chiao.cor(self.minute_open_list[a][-10:],self.minute_open_list[b][-10:]) 
			cor_15 =chiao.cor(self.minute_open_list[a][-30:],self.minute_open_list[b][-30:]) 

		# vol ratio is total vol of 15 min, and 30 min.
		showVolume = False
		if(showVolume):
			sum_a = sum(self.minute_volume_list[a][-15:])
			sum_b =  sum(self.minute_volume_list[b][-15:])
			total_sum = sum_a+sum_b

			vol_ratio_15 = 0.5
			if total_sum != 0:
				vol_ratio_15 = sum_a/total_sum

			sum_a =  sum(self.minute_volume_list[a][-30:])
			sum_b = sum(self.minute_volume_list[b][-30:])
			total_sum = sum_a+sum_b
			vol_ratio_30 = 0.5
			if total_sum != 0:
				vol_ratio_30 = sum_a/total_sum

			sum_a = self.transaction_temp[a]+ sum(self.cur_transaction_list[a][-179:])
			sum_b = self.transaction_temp[b]+ sum(self.cur_transaction_list[b][-179:])
			total_sum = sum_a+sum_b
			tran_ratio_15 = 0.5
			if total_sum != 0:
				tran_ratio_15 = sum_a/total_sum


			sum_a = self.transaction_temp[a]+ sum(self.cur_transaction_list[a][-359:])
			sum_b = self.transaction_temp[b]+ sum(self.cur_transaction_list[b][-359:])
			total_sum = sum_a+sum_b

			tran_ratio_30 = 0.5

			if total_sum != 0:
				tran_ratio_30 = sum_a/total_sum

		# Assign the values to our external read section. 
		with self.readlock:

			self.cur_time.append(t)

			#now the update data. 
			#self.intra_spread.append(self.spread)
			self.roc_1_list.append(self.roc_1)
			self.roc_5_list.append(self.roc_5)
			self.roc_15_list.append(self.roc_15)
			self.intra_spread_seconds.append(self.spread)
			# self.cors_5.append(cor_5)
			# self.cors_15.append(cor_15)

			if self.aggregate_counter% self.minute_counter == 0:
				self.intra_spread.append(self.spread)
				self.intra_spread_MA5.append(chiao.mean(self.intra_spread[-5:]))
				self.intra_spread_MA15.append(chiao.mean(self.intra_spread[-15:]))

		#print("Legnth check",len(self.cur_time),len(self.intra_spread),len(self.roc),len(self.cors_10),len(self.vol_ratio_15))

	# integrated graphing conponent. 
	#def graph(self):


if len(sys.argv) ==1:
	symbols = ["SPY.AM","QQQ.NQ"]
	readlock = threading.Lock()
	test = Pair_trading_processor(symbols,1,TESTMODE,readlock)
	test.start()
	# while True:
	# 	x=1

else:
	symbols = sys.argv[1].split(",")
	readlock = threading.Lock()

	test = Pair_trading_processor(symbols,1,REALMODE,readlock)
	test.start()

	#test = Pair_trading_processor(symbols,3,TESTMODE,readlock)






import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from matplotlib.dates import DateFormatter
from scipy.stats import skew,kurtosis
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick

outlier = dict(linewidth=3, color='darkgoldenrod',marker='o')
plt.style.use("seaborn-darkgrid")
f = plt.figure(1,figsize=(10,12))
f.canvas.set_window_title('SPREAD MONITOR')
min_form = DateFormatter("%H:%M")
gs = f.add_gridspec(4, 3)

a=[1,2,1]
b=[1,2,3]

#set the self plot

spread = f.add_subplot(gs[0,:])
spread.tick_params(axis='both', which='major', labelsize=8)
spread.set_title('IntraDay Spread')

m1 = f.add_subplot(gs[3,:])
m1.tick_params(axis='both', which='major', labelsize=8)
m1.set_title('1 min Spread')


m_dis,w_dis,roc1l,roc5l,roc15l = SVF.find_info(symbols)


max_spread_d = f.add_subplot(gs[1,0])
max_spread_d.set_title('Max Spread Today')
max_spread_d.boxplot([], flierprops=outlier,vert=False, whis=1)

max_spread_w = f.add_subplot(gs[1,1])
max_spread_w.set_title('Max Spread Weekly')
max_spread_w.boxplot(w_dis, flierprops=outlier,vert=False, whis=1)

max_spread_m = f.add_subplot(gs[1,2])
max_spread_m.set_title('Max Spread Monthly')
max_spread_m.boxplot(m_dis, flierprops=outlier,vert=False, whis=1)


roc1 = f.add_subplot(gs[2,0])
roc1.set_title('Speed 1 min')
roc1.boxplot(roc1l, flierprops=outlier,vert=False, whis=2.5)

roc5 = f.add_subplot(gs[2,1])
roc5.set_title('Speed 5 min')
roc5.boxplot(roc5l, flierprops=outlier,vert=False, whis=1.5)

roc15 =f.add_subplot(gs[2,2])
roc15.set_title('Speed 15 min')
roc15.boxplot(roc15l, flierprops=outlier,vert=False, whis=1.5)



def update(self,PT:Pair_trading_processor,readlock):

	global roc1
	global roc5
	global roc15
	global max_spread_d
	global max_spread_w
	global max_spread_m

	with readlock:
		cur_time = PT.cur_minute_list[:]
		intra_spread = PT.intra_spread[:]
		spread5 = PT.intra_spread_MA5[:]
		spread15 = PT.intra_spread_MA15[:]

		cur_second = PT.cur_time[:]
		min1 = PT.roc_1_list[:]


	roc_1 = PT.roc_1
	roc_5 = PT.roc_5
	roc_15 = PT.roc_15
	cur_spread = PT.spread
	today_spread_dis = PT.max_spread_bin_today



	if(len(cur_time)>1):
		cur_minute = pd.to_datetime(cur_time,format='%H:%M')

		spread.clear()
		spread.plot(cur_minute,intra_spread,"y",label="current spread")
		spread.plot(cur_minute[-1],cur_spread,"r^")
		spread.plot(cur_minute,spread5,"r",label="MA5")
		spread.plot(cur_minute,spread15,"b",label="MA15")
		spread.xaxis.set_major_formatter(min_form)
		spread.yaxis.set_major_formatter(mtick.PercentFormatter())
		spread.legend()

		m1.clear()
		m1.plot(cur_minute,min1,"y",label="current spread")
		m1.xaxis.set_major_formatter(min_form)

		max_spread_d.clear()
		max_spread_d.set_title('Cur Spread Distribution')
		max_spread_d.boxplot(intra_spread, flierprops=outlier,vert=False, whis=1)
		max_spread_d.axvline(x=cur_spread,color="r")

		max_spread_w.clear()
		max_spread_w.set_title('W Spread Distribution')
		max_spread_w.boxplot(w_dis, flierprops=outlier,vert=False, whis=1)
		max_spread_w.axvline(x=cur_spread,color="r")

		max_spread_m.clear()
		max_spread_m.set_title('M Spread Distribution')
		max_spread_m.boxplot(m_dis, flierprops=outlier,vert=False, whis=1)
		max_spread_m.axvline(x=cur_spread,color="r")


		roc1.clear()
		roc1.set_title('Speed 1 min')
		roc1.boxplot(roc1l, flierprops=outlier,vert=False, whis=1.5)
		roc1.axvline(x=roc_1,color="r")

		roc5.clear()
		roc5.set_title('Speed 5 min')
		roc5.axvline(x=roc_5,linewidth=2,color="r")
		roc5.boxplot(roc5l, flierprops=outlier,vert=False, whis=1.5)

		roc15.clear()
		roc15.set_title('Speed 15 min')
		roc15.boxplot(roc15l, flierprops=outlier,vert=False, whis=1.5)
		roc15.axvline(x=roc_15,linewidth=2,color="r")


ani = FuncAnimation(f,update,fargs=(test,readlock),interval=1000)

plt.tight_layout()
plt.show()







































































































#plt.show()


