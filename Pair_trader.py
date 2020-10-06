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
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

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

		self.intra_spread_MA5_std = []

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

			# UI_pairtrade.update(self, self.readlock)
			print("update graph")
			time.sleep(sleep)


	def aggregate_data(self):

		super().aggregate_data()
		now = datetime.datetime.now()
		t = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))
		# if there is update, use the newest update. else, use old data...
		# need:
		# 1. spread, spread MA5, spread MA15.
		# 2. roc, roc_ma5, roc_ma15
		# 3. vol ratio, 1 , 2 
		# 4. cor  1, 2 
		#### LOTS OF optimization to be made in here. But for now lets just do stupid. 

		a = self.pairs[0]
		b = self.pairs[1]

		spread = self.mean_temp[a] - self.mean_temp[b]

		if self.tosmode == TESTMODE:
			spread += 58
		spread_ma5 = (sum(self.intra_spread[-59:]) + spread)/(len(self.intra_spread[-59:])+1) 
		spread_ma15 = (sum(self.intra_spread[-179:]) + spread)/(len(self.intra_spread[-179:])+1)

		roc = (self.mean_temp[a]-self.init_price[a]) - (self.mean_temp[b] - self.init_price[b])
		roc_ma5 = (sum(self.roc[-59:]) + roc)/(len(self.roc[-59:])+1)
		roc_ma15 = (sum(self.roc[-179:]) + roc)/(len(self.roc[-179:])+1)


		# vol ratio is total vol of 15 min, and 30 min.

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


		# correlation.
		cor_10 = 0
		cor_30 = 0

		if  len(self.cur_minute_price_list[a]) >= 4:
			# print("length:",len(self.cur_price_list[a]),len(self.cur_price_list[b]))
			# print("pass in :",self.cur_price_list[a][-120:],self.cur_price_list[b][-120:])
			# print("pass in :",self.cur_price_list[a][-120:][:-1],self.cur_price_list[b][-120:][:-1])
			cor_10 = chiao.cor(self.cur_price_list[a][-120:],self.cur_price_list[b][-120:]) 
			cor_30 =chiao.cor(self.cur_price_list[a][-360:],self.cur_price_list[b][-360:]) 


		# Assign the values to our external read section. 
		with self.readlock:

			self.cur_time.append(t)

			# for i in self.symbols:
			# 	self.cur_price[i] = self.mean_temp[i]
			# 	self.cur_volume[i] =self.volume_sum_temp[i]
			# 	self.cur_transaction[i] = self.transaction_temp[i]

			# 	self.cur_price_list[i].append(self.mean_temp[i])
			# 	self.cur_volume_list[i].append(self.volume_sum_temp[i])
			# 	self.cur_transaction_list[i].append(self.transaction_temp[i])

			#now the update data. 
			self.intra_spread.append(spread)
			self.intra_spread_MA5.append(spread_ma5)
			self.intra_spread_MA5_std.append(np.std(self.intra_spread[-30:]))
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

		print("Legnth check",len(self.cur_time),len(self.intra_spread),len(self.roc),len(self.cors_10),len(self.vol_ratio_15))

	# integrated graphing conponent. 
	#def graph(self):


if len(sys.argv) ==1:
	symbols = ["SPY.AM","QQQ.NQ"]
	readlock = threading.Lock()
	test = Pair_trading_processor(symbols,5,TESTMODE,readlock)
	test.start()

else:
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


# target=TOS_init, args=(Symbol,Price,Volume), daemon=True
#t1 = threading.Thread(target=test.start_function,args=(), daemon=True)
# t1.start()
#cur_minute = pd.to_datetime(cur_time,format='%H:%M:%S')
####




### PAIR TRADER MOUDULE  ##############################



# ############################################################################

GAP =pd.read_csv('data/SPYQQQpair.csv')


month_dates = pd.to_datetime(GAP["timestamp"],format='%m/%d/%Y %H:%M')
month_GAP = GAP["price_gap"]

m_dat = np.array([np.float32(i) for i in range(len(month_dates))])
m_linefit = np.polyfit(m_dat,month_GAP,1)
m_slope = np.float32(m_linefit[0])
m_intcep = np.float32(m_linefit[1])
m_regression_line = m_intcep+m_slope*m_dat
m_STD = chiao.MovingStd(month_GAP,600)
m_SMA = chiao.SMA(list(month_GAP),600)
m_std= np.std(month_GAP)
m_reg = [m_regression_line[-1]]



week = 960*5
week_dates = month_dates[-week:]
week_GAP = list(month_GAP[-week:])

w_dat = np.array([np.float32(i) for i in range(len(week_dates))])
w_linefit = np.polyfit(w_dat,week_GAP,1)
w_slope = np.float32(w_linefit[0])
w_intcep = np.float32(w_linefit[1])
w_regression_line = w_intcep+w_slope*w_dat
w_STD = chiao.MovingStd(week_GAP,120)
w_SMA = chiao.SMA(list(week_GAP),120)
w_std= np.std(week_GAP)
w_reg = [w_regression_line[-1]]


day = 960

d_dates = week_dates[-day:]
d_GAP = week_GAP[-day:]

d_dat = np.array([np.float32(i) for i in range(len(d_dates))])
d_linefit = np.polyfit(d_dat,d_GAP,1)
d_slope = np.float32(d_linefit[0])
d_intcep = np.float32(d_linefit[1])
d_regression_line = d_intcep+d_slope*d_dat
d_STD = chiao.MovingStd(d_GAP,30)
d_SMA = chiao.SMA(list(d_GAP),30)
d_std = np.std(d_GAP)
d_reg = [d_regression_line[-1]]

dm=np.arange(len(month_dates))
d=np.arange(len(week_dates))
d2=np.arange(len(d_dates))

newd = [len(d)]
newd2 = [len(d2)]
newm = [len(dm)]


#optimize month data 
month_GAP = month_GAP[::4]
dm = dm[::4]
m_STD = m_STD[::4]
m_SMA =m_SMA[::4]
m_regression_line = m_regression_line[::4]


newGAP = [week_GAP[-1]]


def equidate_ax(fig, ax, dates, fmt="%m-%d"):    
    N = len(dates)
    def format_date(index, pos):
        index = np.clip(int(index + 0.5), 0, N - 1)
        return dates[index].strftime(fmt)
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_xlabel("dates")
    fig.autofmt_xdate()


############################################################################

class alert_val():

	def __init__(self,symbols):
		self.vals = {}
		for i in symbols:
			self.vals[i] = []
		self.pair = []

	def set_symbol(self,symbol,lst):
		self.vals[symbol]=lst[:]

	def set_pair(self,lst):
		self.pair=lst[:]
#current values 
s= []
q= []

#pair values 
p=[]



############################################################################

plt.style.use("seaborn-darkgrid")
f = plt.figure(1,figsize=(10,15))
f.canvas.set_window_title('SPREAD MONITOR')


m_spread = f.add_subplot(621)

m_spread.set_title("Intraday Spread - Past one month",fontsize=8)
m_spread.plot(dm,month_GAP,"r",label="Spread")
m_spread.plot(dm,m_SMA,"c",label="Spread SMA10")
m_spread.plot(dm,m_regression_line,"b",label="Regression line",linewidth=1)
m_spread.fill_between(dm, m_regression_line-2*m_std,m_regression_line+2*m_std,alpha=0.23,label="Price gap deviation zone")
m_spread.tick_params(axis='both', which='major', labelsize=8)
equidate_ax(f,m_spread,list(month_dates))

w_spread = f.add_subplot(623)

w_spread.set_title("Intraday Spread - Past one Week",fontsize=8)
w_spread.plot(d,week_GAP,"r",label="Spread")
w_spread.plot(d,w_SMA,"c",label="Spread SMA10")
w_spread.plot(d,w_regression_line,"b",label="Regression line",linewidth=1)
w_spread.fill_between(d, w_regression_line-2*w_std,w_regression_line+2*w_std,alpha=0.23,label="Price gap deviation zone")
w_spread.tick_params(axis='both', which='major', labelsize=8)
equidate_ax(f,w_spread,list(week_dates))


d_spread = f.add_subplot(625)

d_spread.set_title("Intraday Spread - Past one Day",fontsize=8)
d_spread.plot(d2,d_GAP,"r",label="Spread")
d_spread.plot(d2,d_SMA,"c",label="Spread SMobjectA10")
d_spread.plot(d2,d_regression_line,"b--",label="Regression line",linewidth=1)
d_spread.fill_between(d2, d_SMA-2*d_std,d_SMA+2*d_std,alpha=0.23,label="Price gap deviation zone")
d_spread.tick_params(axis='both', which='major', labelsize=8)


daily_spread = f.add_subplot(627)
daily_spread.set_title("Intraday Spread - Today",fontsize=8)
daily_spread.tick_params(axis='both', which='major', labelsize=8)


yrange = [i/10 +0. for i in range(0,11,2)]
yrange_cor = [round(i/10 +-1.,2) for i in range(0,21,2)]

vol15 = f.add_subplot(6,4,17)
vol15.set_title("Volume Ratio, period 1 min",fontsize=8)
vol15.tick_params(axis='both', which='major', labelsize=8)
vol15.locator_params(axis='x', nbins=4)
vol15.set_yticks(yrange)


vol30 = f.add_subplot(6,4,18)
vol30.set_title("Volume Ratio, period 5 min",fontsize=8)
vol30.tick_params(axis='both', which='major', labelsize=8)
vol30.locator_params(axis='x', nbins=4)
vol30.set_ylim([0,1])


cor15 = f.add_subplot(6,4,21)
cor15.set_title("Moving Correlation, period 3 min",fontsize=8)
cor15.tick_params(axis='both', which='major', labelsize=8)
cor15.locator_params(axis='x', nbins=6)
cor15.set_ylim([0,1])

cor30 = f.add_subplot(6,4,22)
cor30.set_title("Moving Correlation, period 15 min",fontsize=8)
cor30.tick_params(axis='both', which='major', labelsize=8)
cor30.locator_params(axis='x', nbins=6)
cor30.set_ylim([0,1])


min_form = DateFormatter("%H:%M")
daily_spread.xaxis.set_major_formatter(min_form)
vol15.xaxis.set_major_formatter(min_form)
vol30.xaxis.set_major_formatter(min_form)
cor15.xaxis.set_major_formatter(min_form)
cor30.xaxis.set_major_formatter(min_form)


alert_text = "alert window:                                                                                             \n"
alert_info = \
"                                                                          \n\
                                                                           \n\
                                                                           \n\
                                                                           \n"

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# plt.text(0.5, 0.81, text+info, fontsize=11, transform=plt.gcf().transFigure,bbox=props, verticalalignment='center')

#######

###################################################


plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace= 0.65)



def update(self,PT:Pair_trading_processor,readlock):

	global dates
	global GAP
	global SMA
	global hist_spread
	global f
	global props

	with readlock:
		
		cur_time = PT.cur_time		

		if(len(cur_time)>1):

			cur_minute = pd.to_datetime(cur_time,format='%H:%M:%S')

			vol_15 = PT.vol_ratio_15
			vol_30 = PT.vol_ratio_30
			cor_15 = PT.cors_10
			cor_30 = PT.cors_30

			intra_spread = PT.intra_spread
			intra_spread5 =  np.array(PT.intra_spread_MA5)
			intra_spread15 = PT.intra_spread_MA15

			intra_std = np.array(PT.intra_spread_MA5_std)


			tran_ratio_15 = PT.tran_ratio_15
			tran_ratio_30 = PT.tran_ratio_30

			newGAP.append(intra_spread[-1])

			newd.append(newd[-1]+1)
			newd2.append(newd2[-1]+1)
			newm.append(newm[-1]+1)

			d_reg.append(d_intcep+d_slope*newd2[-1])
			w_reg.append(w_intcep+w_slope*newd[-1])
			m_reg.append(m_intcep+m_slope*newm[-1])


			#GAP.append(PT.init_price["SPY.AM"] -  PT.init_price["QQQ.NQ"])
			#print("length check start:",len(cur_time),len(vol_15),len(vol_30),len(cor_15),len(cor_30),len(cor_15),len(intra_spread))
			m_spread.clear()
			m_spread.plot(dm,month_GAP,"r",label="Spread")
			m_spread.plot(dm,m_SMA,"c",label="Spread SMobjectA10")
			m_spread.plot(dm,m_regression_line,"b--",label="Regression line",linewidth=1)
			m_spread.fill_between(dm, m_SMA-2*m_std,m_SMA+2*m_std,alpha=0.23,label="Price gap deviation zone")
			m_spread.tick_params(axis='both', which='major', labelsize=8)

			m_spread.plot(newm,newGAP,"blue",label="Spread") 
			m_spread.plot(newm,m_reg,"b--",alpha=0.5) 
			#conituation of regression. SMA, bollinger 


			cur = round((newGAP[-1] - m_reg[-1])/m_std,2)
			t =""
			if cur>=0:
				t = "+"+str(cur)
			else:
				t = "-"+str(cur)

			# How many STD away from Mean?
			# 
			m_spread.set_title("Last 1 month: "+ t+" stds from Regression line",fontsize=8)
			#GAP.append(PT.init_price["SPY.AM"] -  PT.init_price["QQQ.NQ"])
			#print("length check start:",len(cur_time),len(vol_15),len(vol_30),len(cor_15),len(cor_30),len(cor_15),len(intra_spread))
			w_spread.clear()
			w_spread.plot(d,week_GAP,"r",label="Spread")
			w_spread.plot(d,w_SMA,"c",label="Spread SMobjectA10")
			w_spread.plot(d,w_regression_line,"b--",label="Regression line",linewidth=1)
			w_spread.fill_between(d, w_SMA-2*w_std,w_SMA+2*w_std,alpha=0.23,label="Price gap deviation zone")
			w_spread.tick_params(axis='both', which='major', labelsize=8)

			w_spread.plot(newd,newGAP,"blue",label="Spread") 
			w_spread.plot(newd,w_reg,"b--",alpha=0.5) 
			#conituation of regression. SMA, bollinger 


			cur = round((newGAP[-1] - w_reg[-1])/w_std,2)
			t =""
			if cur>=0:
				t = "+"+str(cur)
			else:
				t = "-"+str(cur)

			# How many STD away from Mean?
			# 
			w_spread.set_title("Last 5 days: "+ t+" stds from Regression line",fontsize=8)

			#w_spread.set_title("Intraday Spread - Past one Week: Current:"+str(GAP[-1]))
			#w_spread.legend(loc="lower left",fontsize=7)
			#equidate_ax(f,w_spread,list(week_dates))
			d_spread.clear()
			d_spread.plot(d2,d_GAP,"r",label="Spread")
			d_spread.plot(d2,d_SMA,"c",label="Spread SMobjectA10")
			d_spread.plot(d2,d_regression_line,"b--",label="Regression line",linewidth=1)
			d_spread.fill_between(d2, d_SMA-2*d_std,d_SMA+2*d_std,alpha=0.23,label="Price gap deviation zone")
			d_spread.tick_params(axis='both', which='major', labelsize=8)

			d_spread.plot(newd2,newGAP,"blue",label="Spread") 

			# Continuation of the graph 
			d_spread.plot(newd2,d_reg,"b--",alpha=0.5) 


			cur = round((newGAP[-1] - d_reg[-1])/d_std,2)
			t =""
			if cur>=0:
				t = "+"+str(cur)
			else:
				t = str(cur)


			d_spread.set_title("Last 24 Hours: "+ t+" stds from Regression",fontsize=8)


			#text = report(SPY[-1],QQQ[-1],SMA[-1],STD[-1])
			daily_spread.clear()
			daily_spread.plot(cur_minute,intra_spread,"r",label="current spread")
			daily_spread.plot(cur_minute,intra_spread5,"b",label="MA5")
			daily_spread.fill_between(cur_minute,intra_spread5-2*intra_std,intra_spread5+2*intra_std,alpha=0.23,label="Price gap deviation zone")

			#daily_spread.plot(cur_minute,intra_spread15,"c",label="MA15")
			
			if intra_std[-1]!=0:
				cur = round((intra_spread[-1] - intra_spread5[-1])/intra_std[-1],2)
			else:
				cur = 0


			t =""
			if cur>=0:
				t = "+"+str(cur)
			else:
				t = str(cur)

			daily_spread.set_title("Current: "+ t+" stds from Mean",fontsize=8)

			daily_spread.legend(fontsize=6,loc="upper left")

			if (len(cur_minute)==len(vol_15) and len(vol_15)>5):

				vol15.clear()
				vol15.plot(cur_minute,vol_15,"b",label="Volume Ratio",linewidth=1)
				vol15.plot(cur_minute,tran_ratio_15,"r",label="Transaction Ratio",linewidth=1)
				vol15.plot(cur_minute,[0.5 for i in range(len(cur_minute))],"c--",label="Middle point",linewidth=1)
				vol15.set_yticks(yrange)

				vol15.set_title("Volume&Transaction Ratio 1 min: Current : "+ str(round(vol_15[-1],2)),fontsize=8)

				vol30.clear()
				vol30.plot(cur_minute,vol_30,"b",label="Volume Ratio")
				vol30.plot(cur_minute,tran_ratio_30,"r",label="Transaction Ratio")
				vol30.plot(cur_minute,[0.5 for i in range(len(cur_minute))],"c--",label="Middle point",linewidth=1)
				vol30.set_yticks(yrange)

				vol30.set_title("Volume&Transaction Ratio 5 min: Current : "+ str(round(vol_30[-1],2)),fontsize=8)

				cor15.clear()
				cor15.plot(cur_minute[-30:],cor_15[-30:])

				cor15.set_yticks(yrange_cor)
				cor15.set_title("Correlation 3 min: Current : "+ str(round(cor_15[-1],2)),fontsize=8)

				cor30.clear()
				cor30.plot(cur_minute[-30:],cor_30[-30:])
				cor30.set_yticks(yrange_cor)
				cor30.set_title("Correlation 15 min: Current : "+ str(round(cor_30[-1],2)),fontsize=8)


				# xtick = cur_time[-30:]
				# if len(xtick)>6:
				# 	xtick = cur_time[::len(cur_time)//3]

				# vol15.set_xticks(xtick)
				# vol30.set_xticks(xtick)
				# cor15.set_xticks(xtick)
				# cor30.set_xticks(xtick)

				#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

				vol15.legend(fontsize=6,loc="upper left")
				vol30.legend(fontsize=6,loc="upper left")

				#print("Correlation check:",cor_15,cor_30)

				min_form = DateFormatter("%H:%M")
				daily_spread.xaxis.set_major_formatter(min_form)

				vol15.xaxis.set_major_formatter(min_form)
				vol30.xaxis.set_major_formatter(min_form)
				cor15.xaxis.set_major_formatter(min_form)
				cor30.xaxis.set_major_formatter(min_form)


			#plt.text(0.1, 0.81, alert_text+alert_info, fontsize=11, transform=plt.gcf().transFigure,bbox=props, verticalalignment='center')

			# vol15.set_xticks(xtick)
			# vol30.set_xticks(xtick)
			# cor15.set_xticks(xtick)
			# cor30.set_xticks(xtick)


ani = FuncAnimation(f,update,fargs=(test,readlock),interval=5000)


plt.show()




















































































































#plt.show()


