import threading
import time
import pandas as pd
import numpy as np
import datetime
import Functions as chiao
from Data_processor import Data_processor

import sys
import os
##########################################



import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as mticker
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import Functions as chiao





#############################################
TESTMODE = False
REALMODE = True


# 1. QUESTION IS. HOW DO I FEED THOSE DATA FEED TO UI?

# 2. QUESTION IS. WHAT DA FUCK AM I CALCULATING 

class Pair_trading_processor(Data_processor):

	# Requires more - Spread, Vol Ratio, and ROC, and Cor. 
	def __init__(self,symbols,interval,tos_mode,readlock):
		super().__init__(symbols,interval,tos_mode,readlock)

		self.pairs = (symbols[0],symbols[1])

		self.intra_spread = []
		self.intra_spread_MA5 = []
		self.intra_spread_MA15 = []

		self.vol_ratio_15 = []
		self.vol_ratio_30 = []

		self.tran_ratio_15 = []
		self.tran_ratio_30 = []

		self.roc = []
		self.roc_15 = []
		self.roc_30 = []


		self.cors_10 = []
		self.cors_30 = []

		
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

	def start_function(self):

		print("Console (PT): Pair trading moudule begins. ")
		super().tos_start()

		interval = self.interval
		while True:

			current_time = time.time()

			self.aggregate_data()

			lag = (time.time() - current_time)
			sleep = self.interval
			if interval*1000-lag> 0 : sleep = (interval*1000-lag)/1000
			print("\nConsole (PT): Processing for ",round(lag*1000,2),"ms , Sleep for",round(sleep,5),"s \n")

			###if pair trade mode is on, display the info###

			time.sleep(sleep)




	def aggregate_data(self):

		# This is one executation of the INTERVAL loop. 

		# 0. Initialize the values we need.
		#col=['time','mean','volume','open','close','high','low','vwap','std',"transaction"]

		# 1. Take the values from the bin. 
		with self.binlock:
			for i in self.symbols:
				print("Console (DP): Processing",i,"transaction counts:",len(self.price[i]),len(self.volume[i]))
				self.price_temp[i] = self.price[i][:]
				self.volume_temp[i] = self.volume[i][:]
				self.price[i] = []
				self.volume[i] = []


		# Calculate the values and clear out the bins
		now = datetime.datetime.now()
		t = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))
		# if there is update, use the newest update. else, use old data...


		for i in self.symbols:
			
				if (len(self.price_temp[i])>0):
					self.mean_temp[i] = chiao.mean(self.price_temp[i])
					self.volume_sum_temp[i] = sum(self.volume_temp[i])
					self.transaction_temp[i] = len(self.price_temp[i])
					# open_ = self.price_temp[i][0]
					# close_ = self.price_temp[i][-1]
					# high_ = max(pself.rice_temp[i])
					# low_ = min(self.price_temp[i])
					# vwap_ = chiao.vwap(self.price_temp[i],self.volume_temp[i]) 
					# std_ = np.std(self.price_temp[i])
					# clear off the thing. 
					# d = pd.DataFrame([[t,mean_,volume_,open_,close_,high_,low_,vwap_,std_,tran_]], columns=col)

				else:
					self.volume_sum_temp[i] = 0
					self.transaction_temp[i] = 0

				print("Console (PT): ",i,":price",round(self.mean_temp[i],4),"volume",self.volume_sum_temp[i],"transaction",self.transaction_temp[i])


		### Now it's time to do the calculation on Pair stuff.

		# need:
		# 1. spread, spread MA5, spread MA15.
		# 2. roc, roc_ma5, roc_ma15
		# 3. vol ratio, 1 , 2 
		# 4. cor  1, 2 


		#### LOTS OF optimization to be made in here. But for now lets just do stupid. 

		a = self.pairs[0]
		b = self.pairs[1]

		spread = self.mean_temp[a] - self.mean_temp[b]
		spread_ma5 = (sum(self.intra_spread[-59:]) + spread)/(len(self.intra_spread[-59:])+1)
		spread_ma15 = (sum(self.intra_spread[-179:]) + spread)/(len(self.intra_spread[-179:])+1)

		roc = (self.mean_temp[a]-self.init_price[a]) - (self.mean_temp[b] - self.init_price[b])
		roc_ma5 = (sum(self.roc[-59:]) + roc)/(len(self.roc[-59:])+1)
		roc_ma15 = (sum(self.roc[-179:]) + roc)/(len(self.roc[-179:])+1)


		#print(self.volume_sum_temp[a],self.cur_volume_list[a])
		# vol ratio is total vol of 15 min, and 30 min.

		sum_a = self.volume_sum_temp[a]+  sum(self.cur_volume_list[a][-179:])
		sum_b = self.volume_sum_temp[b]+ sum(self.cur_volume_list[b][-179:])
		total_sum = sum_a+sum_b

		vol_ratio_15 = 0.5
		if total_sum != 0:
			vol_ratio_15 = sum_a/total_sum

		sum_a =  self.volume_sum_temp[a]+  sum(self.cur_volume_list[a][-179:])
		sum_b = self.volume_sum_temp[b]+ sum(self.cur_volume_list[b][-359:])
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


		# correlation.
		cor_10 = 0
		cor_30 = 0

		if len(self.cur_price_list[a]) >= 2 and len(self.cur_price_list[a]) >= 4:
			# print("length:",len(self.cur_price_list[a]),len(self.cur_price_list[b]))
			# print("pass in :",self.cur_price_list[a][-120:],self.cur_price_list[b][-120:])
			# print("pass in :",self.cur_price_list[a][-120:][:-1],self.cur_price_list[b][-120:][:-1])
			cor_10 = chiao.cor(self.cur_price_list[a][-120:],self.cur_price_list[b][-120:]) 
			cor_30 =chiao.cor(self.cur_price_list[a][-360:],self.cur_price_list[b][-360:]) 


		# Assign the values to our external read section. 
		with self.readlock:

			self.cur_time.append(t)

			for i in self.symbols:
				self.cur_price[i] = self.mean_temp[i]
				self.cur_volume[i] =self.volume_sum_temp[i]
				self.cur_transaction[i] = self.transaction_temp[i]

				self.cur_price_list[i].append(self.mean_temp[i])
				self.cur_volume_list[i].append(self.volume_sum_temp[i])
				self.cur_transaction_list[i].append(self.transaction_temp[i])


			#now the update data. 
			self.intra_spread.append(spread)
			self.intra_spread_MA5.append(spread_ma5)
			self.intra_spread_MA15.append(spread_ma15)

			self.vol_ratio_15.append(vol_ratio_15)
			self.vol_ratio_30.append(vol_ratio_30)

			self.tran_ratio_15.append(tran_ratio_15)
			self.tran_ratio_30.append(tran_ratio_30)

			self.roc.append(roc)
			self.roc_15.append(roc_ma5)
			self.roc_30.append(roc_ma15)


			self.cors_10.append(cor_10)
			self.cors_30.append(cor_30)

		# print(self.intra_spread)
		# print(self.intra_spread_MA5)
		# print(self.intra_spread_MA15)
		#print("Legnth check",len(self.cur_time),len(self.intra_spread),len(self.roc),len(self.cors_10),len(self.vol_ratio_15))

	# integrated graphing conponent. 
	#def graph(self):



mode  = sys.argv[1]

symbols = ["SPY.AM","QQQ.NQ"]
readlock = threading.Lock()

if mode == "t":
	test = Pair_trading_processor(symbols,3,TESTMODE,readlock)
	test.start()
elif mode ==  "r":
	test = Pair_trading_processor(symbols,5,REALMODE,readlock)
	test.start()
if mode != "t" and  mode !=  "r":
	print("Console: Wrong input")
	os._exit(1)
#test = Pair_trading_processor(symbols,3,TESTMODE,readlock)

test = Pair_trading_processor(symbols,5,REALMODE,readlock)
test.start()


# target=TOS_init, args=(Symbol,Price,Volume), daemon=True
#t1 = threading.Thread(target=test.start_function,args=(), daemon=True)
# t1.start()
#cur_minute = pd.to_datetime(cur_time,format='%H:%M:%S')
####




### PAIR TRADER MOUDULE  ##############################




#### FUNCTION 1 : COMPUTING PAIR TRADE INFORMATION 

# for std. i need a list of the means. I don't need the list anymore.


# CUR_GAP.
	#STD multiple
	#STD multiple
	#STD multiple
	#STD
# Volume ratio
# Correlation 
# ROC ratio  - On different MA lines. 

# 5 MIN MA  (-60)
# 15 MIN MA  (-180)
# 30 MIN MA  (-360)
# 60 MIN MA  (-720)

# 1 min volume sum?  just a number 



#pd.to_datetime(t,format='%m/%d/%Y %H:%M')


#### FUNCTION 2:  GRAPHING



	
plt.style.use("seaborn-darkgrid")
f = plt.figure(1,figsize=(10,15))
f.canvas.set_window_title('SPREAD MONITOR')


def report(spy,qqq,sma,std):

	n = round(((spy-qqq)-sma)/std,2)

	text = ""
	if n >=0:
		text = "+" + str(n) + "STD away from the regression line"
	else:
		text = "-" + str(n) + "STD away from the regression line"

	return text


SPY = np.array([311.56, 310.19, 310.37, 308.56, 310.68, 312.03, 304.12, 307.31, 300.01, 304.43, 308.57, 310.57, 312.18, 316.99, 313.72, 316.12, 314.42, 317.61, 314.81, 318.89, 321.865, 320.81, 321.67, 324.36, 324.96, 326.82, 322.935, 320.86, 323.18, 321.2, 325.09, 323.98, 326.55, 328.76, 330.02, 332.06, 334.31, 334.55, 335.55, 332.82, 337.42, 336.86, 336.86, 337.88, 338.62, 337.22, 338.25, 339.44, 342.94, 344.0999, \
347.56, 348.29, 350.54, 349.35, 352.56, 357.68, 345.41, 342.6, 333.26, 339.76,339.89,334.06,338.46, 342.14	,341.51,333.56,335.37,335.37])
QQQ = np.array([242.53, 243.14, 243.87, 243.74, 246.77, 248.73, 243.78, 246.08, 240.08, 242.77, 247.28, 250.43, 252.11, 258.39, 256.56, 259.94, 262.06, 264.01, 258.53, 260.41, 260.78, 258.98, 259.38, 266.79, 264.05, 264.92, 257.95, 255.44, 260.09, 256.76, 259.83, 261.16, 265.84, 269.31, 270.44, 271.11, 274.585, 271.5, 270.28, 265.21, 271.93, 272.48, 272.22, 275.27, 277.962, 276.14, 279.88, 281.85, 283.61, 285.82, \
291.88, 290.99, 292.5, 294.99, 299.89, 302.73, 287.21, 283.47, 270.01, 277.78,272.34	,270.45,275.16	, 278.88	,279.88	,267.55	,271.79	,271.79])
GAP = SPY-QQQ
STD = chiao.MovingStd(GAP,20)
SMA = chiao.SMA(GAP,10)

dates = np.array(['06/16/2020', '06/17/2020', '06/18/2020', '06/19/2020', '06/22/2020', '06/23/2020', '06/24/2020', '06/25/2020', '06/26/2020', '06/29/2020', '06/30/2020', '07/01/2020', '07/02/2020', '07/06/2020', '07/07/2020', '07/08/2020', '07/09/2020', '07/10/2020', '07/13/2020', '07/14/2020', '07/15/2020', '07/16/2020', '07/17/2020', '07/20/2020', '07/21/2020', '07/22/2020', '07/23/2020', '07/24/2020', '07/27/2020', '07/28/2020', '07/29/2020', '07/30/2020', '07/31/2020', '08/03/2020', '08/04/2020', '08/05/2020', '08/06/2020', '08/07/2020', '08/10/2020', '08/11/2020', '08/12/2020', '08/13/2020', '08/14/2020', '08/17/2020', '08/18/2020', '08/19/2020', '08/20/2020', '08/21/2020', '08/24/2020', '08/25/2020', '08/26/2020', '08/27/2020', '08/28/2020', '08/31/2020', '09/01/2020', '09/02/2020', '09/03/2020', \
'09/04/2020', '09/08/2020', '09/09/2020','09/10/2020','09/11/2020','09/14/2020','09/15/2020','09/16/2020','09/17/2020','09/18/2020','09/21/2020'])
dates = pd.to_datetime(dates)

dat = np.array([np.float32(i) for i in range(len(dates))])
linefit = np.polyfit(dat,GAP,1)
slope = np.float32(linefit[0])
intcep = np.float32(linefit[1])
regression_line = intcep+slope*dat




hist_spread = f.add_subplot(521)#add_axes([0.1, 0.1, 0.78, 0.78])
# hist_spread.plot(dates,GAP,"r",label="Spread")
# hist_spread.plot(dates,SMA,"c",label="Spread SMA10")
# hist_spread.fill_between(dates, SMA-2*STD,SMA+2*STD,alpha=0.23,label="Price gap deviation zone")

daily_spread = f.add_subplot(512)
daily_spread.set_title("Intraday Spread",fontsize=8)
daily_spread.tick_params(axis='both', which='major', labelsize=8)


roc = f.add_subplot(513)
roc.set_title("Rate of Change Difference:",fontsize=8)
roc.tick_params(axis='both', which='major', labelsize=8)
roc.locator_params(tight=True, nbins=6)


yrange = [i/10 +0. for i in range(0,11,2)]
yrange_cor = [round(i/10 +-1.,2) for i in range(0,21,2)]

vol15 = f.add_subplot(527)
vol15.set_title("Volume Ratio, period 15 min",fontsize=8)
vol15.tick_params(axis='both', which='major', labelsize=8)
vol15.locator_params(axis='x', nbins=4)
vol15.set_yticks(yrange)


vol30 = f.add_subplot(528)
vol30.set_title("Volume Ratio, period 30 min",fontsize=8)
vol30.tick_params(axis='both', which='major', labelsize=8)
vol30.locator_params(axis='x', nbins=4)
vol30.set_ylim([0,1])


cor15 = f.add_subplot(529)
cor15.set_title("Moving Correlation, period 15 min",fontsize=8)
cor15.tick_params(axis='both', which='major', labelsize=8)
cor15.locator_params(axis='x', nbins=6)
cor15.set_ylim([0,1])

cor30 = f.add_subplot(5,2,10)
cor30.set_title("Moving Correlation, period 30 min",fontsize=8)
cor30.tick_params(axis='both', which='major', labelsize=8)
cor30.locator_params(axis='x', nbins=6)
cor30.set_ylim([0,1])
# cor2 = f.add_subplot(5,2,10)
# cor2.set_title("Moving Correlation, period 15 min",fontsize=8)
# cor2.tick_params(axis='both', which='major', labelsize=8)

#min_form = DateFormatter("%H:%M:%S")
min_form = DateFormatter("%H:%M")
daily_spread.xaxis.set_major_formatter(min_form)
vol15.xaxis.set_major_formatter(min_form)
vol30.xaxis.set_major_formatter(min_form)
cor15.xaxis.set_major_formatter(min_form)
cor30.xaxis.set_major_formatter(min_form)


alert_text = "alert window:                                                                            \n"
alert_info = \
"                                                                          \n\
                                                                           \n\
                                                                           \n\
                                                                           \n"

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# plt.text(0.5, 0.81, text+info, fontsize=11, transform=plt.gcf().transFigure,bbox=props, verticalalignment='center')

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace= 0.45)


def update(self,PT:Pair_trading_processor,readlock):

	global dates
	global GAP
	global SMA
	global hist_spread
	global f
	global props

	with readlock:
		
		cur_time = PT.cur_time		

		if(len(cur_time)>2):

			cur_minute = pd.to_datetime(cur_time,format='%H:%M:%S')
			# xtick = cur_time
			# if len(cur_time)>6:
			# 	xtick = cur_time[::len(cur_time)//5]

			vol_15 = PT.vol_ratio_15
			vol_30 = PT.vol_ratio_30
			cor_15 = PT.cors_10
			cor_30 = PT.cors_30

			intra_spread = PT.intra_spread
			intra_spread5 = PT.intra_spread_MA5
			intra_spread15 = PT.intra_spread_MA15

			tran_ratio_15 = PT.tran_ratio_15
			tran_ratio_30 = PT.tran_ratio_30

			roc_ = PT.roc
			roc_15 = PT.roc_15
			GAP[-1] = PT.init_price["SPY.AM"] -  PT.init_price["QQQ.NQ"]

			#print("length check start:",len(cur_time),len(vol_15),len(vol_30),len(cor_15),len(cor_30),len(cor_15),len(intra_spread))
			hist_spread.clear()
			hist_spread.plot(dates,GAP,"r",label="Spread")
			hist_spread.plot(dates,SMA,"c",label="Spread SMA10")
			hist_spread.plot(dates,regression_line,"b",label="Regression line",linewidth=1)
			hist_spread.fill_between(dates, regression_line-2*STD,regression_line+2*STD,alpha=0.23,label="Price gap deviation zone")

			date_form = DateFormatter("%m-%d")
			#a =plt.gca()
			hist_spread.xaxis.set_major_formatter(date_form)
			hist_spread.xaxis.set_major_locator(mdates.DayLocator(interval=15))
			hist_spread.xaxis_date()
			text = report(SPY[-1],QQQ[-1],SMA[-1],STD[-1])

			hist_spread.set_title("Historical Spread: Current "+ text,fontsize=8)
			hist_spread.tick_params(axis='both', which='major', labelsize=8)
			hist_spread.legend(loc="lower left",fontsize=7)

			daily_spread.clear()
			daily_spread.plot(cur_minute,intra_spread,"r",label="current spread")
			daily_spread.plot(cur_minute,intra_spread5,"b",label="MA5")
			daily_spread.plot(cur_minute,intra_spread15,"c",label="MA15")
			
			
			daily_spread.set_title("Intraday Spread: Current : "+ str(round(intra_spread[-1],2)),fontsize=8)

			roc.clear()
			roc.plot(cur_minute,roc_,"r",label="current")
			roc.plot(cur_minute,roc_15,"b",label="MA15")
			roc.set_title("Rate of Change Difference: Current : "+ str(round(roc_[-1],2)),fontsize=8)

			if (len(cur_minute)==len(vol_15) and len(vol_15)>0):

				vol15.clear()
				vol15.plot(cur_minute,vol_15,"b",label="Volume Ratio",linewidth=1)
				vol15.plot(cur_minute,tran_ratio_15,"r",label="Transaction Ratio",linewidth=1)
				vol15.plot(cur_minute,[0.5 for i in range(len(cur_minute))],"c--",label="Middle point",linewidth=1)
				vol15.set_yticks(yrange)

				vol15.set_title("SPY/QQQ Volume&Transaction Ratio 15 min: Current : "+ str(round(vol_15[-1],2)),fontsize=8)

				vol30.clear()
				vol30.plot(cur_minute,vol_30,"b",label="Volume Ratio")
				vol30.plot(cur_minute,tran_ratio_30,"r",label="Transaction Ratio")
				vol30.plot(cur_minute,[0.5 for i in range(len(cur_minute))],"c--",label="Middle point",linewidth=1)
				vol30.set_yticks(yrange)

				vol30.set_title("SPY/QQQ Volume&Transaction Ratio 30 min: Current : "+ str(round(vol_30[-1],2)),fontsize=8)


				cor15.clear()
				cor15.plot(cur_minute,cor_15)
				cor15.set_yticks(yrange_cor)
				cor15.set_title("Correlation 15 min: Current : "+ str(round(cor_15[-1],2)),fontsize=8)

				cor30.clear()
				cor30.plot(cur_minute,cor_30)
				cor30.set_yticks(yrange_cor)
				cor30.set_title("Correlation 30 min: Current : "+ str(round(cor_30[-1],2)),fontsize=8)

				#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
				daily_spread.legend(fontsize=6,loc="upper left")
				vol15.legend(fontsize=6,loc="upper left")
				vol30.legend(fontsize=6,loc="upper left")
				roc.legend(fontsize=6,loc="upper left")

				min_form = DateFormatter("%H:%M")
				daily_spread.xaxis.set_major_formatter(min_form)
				roc.xaxis.set_major_formatter(min_form)
				vol15.xaxis.set_major_formatter(min_form)
				vol30.xaxis.set_major_formatter(min_form)
				cor15.xaxis.set_major_formatter(min_form)
				cor30.xaxis.set_major_formatter(min_form)


			plt.text(0.5, 0.81, alert_text+alert_info, fontsize=11, transform=plt.gcf().transFigure,bbox=props, verticalalignment='center')

			# vol15.set_xticks(xtick)
			# vol30.set_xticks(xtick)
			# cor15.set_xticks(xtick)
			# cor30.set_xticks(xtick)

ani = FuncAnimation(f,update,fargs=(test,readlock),interval=2000)
plt.show()


