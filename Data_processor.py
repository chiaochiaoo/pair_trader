import TOS
import threading
import time
import pandas as pd
import numpy as np
import datetime
import Functions as chiao
import UI_Historical
import multiprocessing
#cur_minute = pd.to_datetime(cur_time,format='%H:%M:%S')
####
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import matplotlib.pyplot as plt 
############### TEST CODE ##########################

TESTMODE = False
REALMODE = True



class Data_processor:

	def __init__(self,symbols,interval,tos_mode,readlock,histo=None):

		self.histo = histo

		self.symbols = symbols
		self.tosmode = tos_mode
		self.interval = interval

		self.cur_time = []
		self.cur_minute_list = []
		self.cur_minute = 0
		self.readlock = readlock

		# minute counter is in how many loops it will become one minute. 
		self.minute_counter = 30//interval 
		self.aggregate_counter = 0

		# This is the bin value, gather, and clean after every interval. Used with TOS. 

		self.binlock = threading.Lock()
		self.tos_registration = False
		self.price ={}
		self.volume = {}

		for i in symbols:
			self.price[i] = []
			self.volume[i] = []

		# This is temporary filed 
		self.price_temp = {}
		self.volume_temp = {}
		self.mean_temp = {}
		self.volume_sum_temp = {}
		self.transaction_temp = {}

		for i in symbols:

			self.price_temp[i] = []
			self.volume_temp[i] = []
			self.mean_temp[i] = 0
			self.volume_sum_temp[i] = 0
			self.transaction_temp[i] = 0

		# old values 

		self.cur_price_list = {}
		for i in symbols:

			self.cur_price_list[i] = []

		# This is the synchronous value, update upon every interval and for external read. 


		self.init_price = {}
		self.cur_price = {}
		self.cur_volume = {}
		self.cur_transaction = {}


		for i in symbols:

			self.init_price[i] =0
			self.cur_price[i] =0
			self.cur_volume[i] =0
			self.cur_transaction[i] =0

		# This is where we keep the original data - for , 30 time period. 
		self.cur_minute_price_list = {}
		self.cur_minute_volume_list = {}
		self.cur_transaction_list = {}


		for i in symbols:

			# this store the movement of all.
			self.cur_minute_price_list[i] = []
			self.cur_minute_volume_list[i] = []
			self.cur_transaction_list[i] = []

		### field for calculating minute data



		#current minute volume
		self.minute_volume_value = {}
		self.minute_volume5_value = {}
		self.minute_volume30_value = {}

		self.minute_volume_list = {}

		for i in symbols:

			self.minute_volume_value[i] = 0
			self.minute_volume5_value[i] = 0
			self.minute_volume30_value[i] = 0

			self.minute_volume_list[i] = []

		#current minute high and low 
		self.minute_high_value = {}
		self.minute_low_value = {}

		self.minute_high_list = {}
		self.minute_low_list = {}


		self.minute_range_value = {}
		self.minute_range5_value = {}
		self.minute_range30_value = {}

		for i in symbols:

			self.minute_high_value[i] = 0
			self.minute_low_value[i] = 0
			self.minute_range_value[i] = 0
			self.minute_range5_value[i] = 0
			self.minute_range30_value[i] = 0

			self.minute_high_list[i] = []
			self.minute_low_list[i] = []

		#

		self.minute_open_value = {}
		self.minute_close_value = {}

		self.minute_open_list = {}
		self.minute_close_list = {}

		self.minute_roc_value = {}
		self.minute_roc5_value = {}
		self.minute_roc30_value = {}

		for i in symbols:

			self.minute_open_value[i] = 0
			self.minute_close_value[i] = 0
			self.minute_roc_value[i] = 0
			self.minute_roc5_value[i] = 0
			self.minute_roc30_value[i] = 0

			self.minute_open_list[i] = []
			self.minute_close_list[i] = []


		self.histo.set_hist(self)
		# ERROR CHECKING ?

 
	def tos_start(self):
		### time to start harvesting 

		tos = threading.Thread(target=TOS.TOS_init, args=(self.symbols,self.price,self.volume,self.binlock,self.tosmode), daemon=True)
		tos.start()

		### WE need to wait until bin of each symbol get something. 

		check = 0
		while check != len(self.symbols):
			check = 0
			with self.binlock:
				for i in self.symbols:
					if len(self.price[i])>0:
						self.init_price[i] = chiao.mean(self.price[i])
						check += 1

		print("Console (DP): All data from each symbols received, data processing begins. ")


		return True



	def start(self):
		print("Console (DP): Thread created, ready to start")
		t1 = threading.Thread(target=self.start_function, daemon=True)
		t1.start()
		print("Console (DP): Thread running. Continue:")


	def start_function(self):

		self.tos_start()

		interval = self.interval

		#Sync second. 
		while True:
			now = datetime.datetime.now()
			if (now.second>45) or (now.second<15):
				break


		now = datetime.datetime.now()
		t = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))

		print("Console (DP): Processing begins at",t)
		with self.binlock:
			for i in self.symbols:

				#print("Console (DP): Processing",i,"transaction counts:",len(self.price[i]),len(self.volume[i]))
				self.price[i] = []
				self.volume[i] = []
		#


		while True:

			current_time = time.time()

			self.aggregate_data()

			lag = (time.time() - current_time)
			sleep = self.interval
			if interval*1000-lag> 0 : sleep = (interval*1000-lag)/1000

			print("\nConsole (DP): Processing for ",round(lag*1000,2),"ms , Sleep for",round(sleep,5),"s \n")
			print("\nConsole (DP): ",self.aggregate_counter,self.minute_counter,"\n")
			###if pair trade mode is on, display the info###

			time.sleep(sleep)


	def aggregate_data(self):

		# This is one executation of the INTERVAL loop. 

		# 0. Initialize the values we need.
		#col=['time','mean','volume','open','close','high','low','vwap','std',"transaction"]

		# 1. Take the values from the bin. 
		with self.binlock:
			for i in self.symbols:

				#print("Console (DP): Processing",i,"transaction counts:",len(self.price[i]),len(self.volume[i]))
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

				#print("Console (DP): ",i,":price",round(self.mean_temp[i],4),"volume",self.volume_sum_temp[i],"transaction",self.transaction_temp[i],)
				
		# Assign the values to our external read section. 

		with self.readlock:
			for i in self.symbols:
				self.cur_price[i] = self.mean_temp[i]
				self.cur_volume[i] =self.volume_sum_temp[i]
				self.cur_transaction[i] = self.transaction_temp[i]
				
				self.cur_price_list[i].append(self.cur_price[i])
				#i don't need these temporary values for now 
				self.cur_minute_price_list[i].append(self.cur_price[i])
				self.cur_minute_volume_list[i].append(self.cur_volume[i])
				#print("Console (DP): ",i,"minute price count:",len(self.cur_minute_price_list[i]),"minute volume count",len(self.cur_minute_volume_list[i]))


		self.aggregate_counter +=1

			#if a minute is met. SET ALL THESE VALUES. , clear the minute bin.

		if self.aggregate_counter% self.minute_counter == 0:
			with self.readlock:

				for i in self.symbols:
					#take the data from cur_minute_price_list and cur_minute_volume_list
					self.minute_volume_value[i] =sum(self.cur_minute_volume_list[i]) 
					self.minute_volume_list[i].append(self.minute_volume_value[i])

					if len(self.minute_volume_list[i])>=5:
						self.minute_volume5_value[i] = sum(self.minute_volume_list[i][-5:])
					if len(self.minute_volume_list[i])>=30:
						self.minute_volume30_value[i] = sum(self.minute_volume_list[i][-30:])


					#now, range.

					self.minute_high_value[i] = max(self.cur_minute_price_list[i])
					self.minute_low_value[i] = min(self.cur_minute_price_list[i])
					self.minute_high_list[i].append(self.minute_high_value[i])
					self.minute_low_list[i].append(self.minute_low_value[i])

					self.minute_range_value[i] = self.minute_high_value[i]-self.minute_low_value[i]

					if len(self.minute_high_list[i])>=5:
						self.minute_range5_value[i] = max(self.minute_high_list[i][-5:])-min(self.minute_low_list[i][-5:])
					if len(self.minute_high_list[i])>=30:
						self.minute_range30_value[i] = max(self.minute_high_list[i][-30:])-min(self.minute_low_list[i][-5:])


					#Eventually, open and close

						# 1. Setting values.
					self.minute_open_value[i] = self.cur_minute_price_list[i][0]
					self.minute_close_value[i] = self.cur_minute_price_list[i][-1]

					self.minute_open_list[i].append(self.minute_open_value[i])
					self.minute_close_list[i].append(self.minute_close_value[i])

						#2. Cal Roc, Roc5, Roc30
					self.minute_roc_value[i] = self.minute_close_value[i] - self.minute_open_value[i]


					if len(self.minute_open_list[i])>=5:
						self.minute_roc5_value[i] = self.minute_close_list[i][-1] - self.minute_open_list[i][-5]
					if len(self.minute_open_list[i])>=30:
						self.minute_roc30_value[i] = self.minute_close_list[i][-1] - self.minute_open_list[i][-30]


					#clearn the bin
					self.cur_minute_volume_list[i] = []
					self.cur_minute_price_list[i] = []

					print("\nConsole (DP): One Minute ",i,"Volume sum:",self.minute_volume_value[i],self.minute_volume5_value[i],self.minute_volume30_value[i],
						"\n Range",round(self.minute_range_value[i],3),round(self.minute_range5_value[i],3),round(self.minute_range30_value[i],3),
						"\n Roc",round(self.minute_roc_value[i],3),round(self.minute_roc5_value[i],3),round(self.minute_roc30_value[i],3),"\n")

					print("Length: minute open close:",len(self.minute_open_list[i]),len(self.minute_close_list[i]))
					print("Length: volume :",len(self.minute_volume_list[i]),)
					print("Length: range high_ low:",len(self.minute_high_list[i]),len(self.minute_low_list[i]))


			self.histo.set_hist(self)
			#TODO
		#### WRITING BLOCK SAVE TO A CSV FILE ####################



####### USE.

symbols = ["SPY.AM","QQQ.NQ"]
readlock = threading.Lock()
#test = Data_processor(symbols,5,TESTMODE,readlock)


class hist:
	def __init__(self):
		self.minute_volume_value = {}
		self.minute_volume5_value = {}
		self.minute_volume30_value = {}
		self.minute_range_value = {}
		self.minute_range5_value = {}
		self.minute_range30_value = {}
		self.minute_roc_value = {}
		self.minute_roc5_value = {}
		self.minute_roc30_value = {}

	def set_hist(self,d):

		self.minute_volume_value = d.minute_volume_value
		self.minute_volume5_value = d.minute_volume5_value
		self.minute_volume30_value = d.minute_volume30_value
		self.minute_range_value = d.minute_range_value
		self.minute_range5_value = d.minute_range5_value
		self.minute_range30_value = d.minute_range30_value
		self.minute_roc_value = d.minute_roc_value
		self.minute_roc5_value = d.minute_roc5_value
		self.minute_roc30_value = d.minute_roc30_value

		print("CHECK",self.minute_volume_value)

histo = hist()

test = Data_processor(symbols,5,TESTMODE,readlock,histo)

lock = multiprocessing.Lock()



# q = Queue()
# p = Process(target=f, args=(q,))
# p.start()

#UI_Historical.main(histo, symbols,readlock)




















































outlier = dict(markerfacecolor='black', marker='o')
S =pd.read_csv('data/SPYstat.csv')
Q =pd.read_csv('data/QQQstat.csv')

start=S[S['time']=='09:30'].index.values[0]
end=S[S['time']=='16:00'].index.values[0]+1

s_vol1_avg = np.mean(S["v1m"][start:end])
s_vol5_avg = np.mean(S["v5m"][start:end])
s_vol30_avg = np.mean(S["v30m"][start:end])

s_vol1_std = np.std(S["v1m"][start:end])
s_vol5_std = np.std(S["v5m"][start:end])
s_vol30_std = np.std(S["v30m"][start:end])

s_range_avg= np.mean(S["rm"][start:end])
s_range_std= np.std(S["rm"][start:end])

s_range5_avg= np.mean(S["r5m"][start:end])
s_range5_std= np.std(S["r5m"][start:end])

s_range30_avg = np.mean(S["r30m"][start:end])
s_range30_std= np.std(S["r30m"][start:end])

s_roc_avg= np.mean(S["rocm"][start:end])
s_roc_std= np.std(S["rocm"][start:end])

s_roc5_avg= np.mean(S["roc5m"][start:end])
s_roc5_std= np.std(S["roc5m"][start:end])

s_roc30_avg= np.mean(S["roc30m"][start:end])
s_roc30_std= np.std(S["roc30m"][start:end])

start=Q[Q['time']=='09:30'].index.values[0]
end=Q[Q['time']=='16:00'].index.values[0]+1

q_vol1_avg = np.mean(S["v1m"][start:end])
q_vol5_avg = np.mean(S["v5m"][start:end])
q_vol30_avg = np.mean(S["v30m"][start:end])

q_vol1_std = np.std(S["v1m"][start:end])
q_vol5_std = np.std(S["v5m"][start:end])
q_vol30_std = np.std(S["v30m"][start:end])

q_range_avg= np.mean(S["rm"][start:end])
q_range_std= np.std(S["rm"][start:end])

q_range5_avg= np.mean(S["r5m"][start:end])
q_range5_std= np.std(S["r5m"][start:end])

q_range30_avg = np.mean(S["r30m"][start:end])
q_range30_std= np.std(S["r30m"][start:end])

q_roc_avg= np.mean(S["rocm"][start:end])
q_roc_std= np.std(S["rocm"][start:end])

q_roc5_avg= np.mean(S["roc5m"][start:end])
q_roc5_std= np.std(S["roc5m"][start:end])

q_roc30_avg= np.mean(S["roc30m"][start:end])
q_roc30_std= np.std(S["roc30m"][start:end])

plot = []
def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele  
        str1 += "\n"
    
    # return string   
    return str1  

def UI_init(symbols,data_processor):

	global plot
	f = plt.figure(1,figsize=(20,10))
	f.canvas.set_window_title('HISTORICAL COMPARISON_')
	#plot[i] = {}
	plot.append({})
	plot.append({})

	v1a = f.add_subplot(4,7,1)
	v5a = f.add_subplot(4,7,2)
	v30a = f.add_subplot(4,7,3)
	r_a = f.add_subplot(4,7,8)
	r5_a = f.add_subplot(4,7,9)
	r30_a = f.add_subplot(4,7,10)
	roc_a = f.add_subplot(4,7,15)
	roc5_a = f.add_subplot(4,7,16)
	roc30_a = f.add_subplot(4,7,17)

	v1b = f.add_subplot(4,7,5)
	v5b = f.add_subplot(4,7,6)
	v30b = f.add_subplot(4,7,7)
	r_b = f.add_subplot(4,7,12)
	r5_b = f.add_subplot(4,7,13)
	r30_b = f.add_subplot(4,7,14)
	roc_b = f.add_subplot(4,7,19)
	roc5_b = f.add_subplot(4,7,20)
	roc30_b = f.add_subplot(4,7,21)



	plot[0]["v1"]= v1a
	plot[0]["v5"]= v5a
	plot[0]["v30"]= v30a
	plot[0]["r_"]= r_a
	plot[0]["r5_"]= r5_a
	plot[0]["r30_"]= r30_a
	plot[0]["roc_"]= roc_a
	plot[0]["roc5_"]= roc5_a
	plot[0]["roc30_"]= roc30_a

	plot[1]["v1"]= v1b
	plot[1]["v5"]= v5b
	plot[1]["v30"]= v30b
	plot[1]["r_"]= r_b
	plot[1]["r5_"]= r5_b
	plot[1]["r30_"]= r30_b
	plot[1]["roc_"]= roc_b
	plot[1]["roc5_"]= roc5_b
	plot[1]["roc30_"]= roc30_b

	return f

def avline(ax,mean,std,actual):

	#print("AVLINE CHECK:",mean,std,actual)
	if actual != 0:
		z = abs(abs(actual-mean)/std)
		#print("Z score:",z)
		if z>=2:
			ax.axvline(actual,c="r",linewidth=4 ,label='Current Position')
		elif z>=1 and z<2:
			ax.axvline(actual,c="y",linewidth=4 ,label='Current Position')
		else:
			ax.axvline(actual,c="g",linewidth=4 ,label='Current Position')


def update(self,d,symbols,lock):

	now = datetime.datetime.now()
	t = '{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute))

	##lets assume it's 12 hours earlier for test purpose
	t = chiao.get_min(t)  - 1 -  720

	print("Current:",chiao.ts_to_str(t))

	#get values 
	with lock:
		s_v1=d.minute_volume_value[symbols[0]]/1000
		s_v5=d.minute_volume5_value[symbols[0]]/1000
		s_v30=d.minute_volume30_value[symbols[0]]/1000
		s_r1=d.minute_range_value[symbols[0]]
		s_r5=d.minute_range5_value[symbols[0]]
		s_r30=d.minute_range30_value[symbols[0]]
		s_roc=d.minute_roc_value[symbols[0]]
		s_roc5=d.minute_roc5_value[symbols[0]]
		s_roc30= d.minute_roc30_value[symbols[0]]

	print("Value check SPY :\n",s_v1,s_v5,s_v30,"\n",s_r1,s_r5,s_r30,"\n",s_roc,s_roc5,s_roc30)
	
	vol1=literal_eval(S.loc[S['timestamp'] == t]["v1d"].values[0])
	vol1m=S.loc[S['timestamp'] == t]["v1m"].values[0]

	vol1s=S.loc[S['timestamp'] == t]["v1s"].values[0]

	vol5=literal_eval(S.loc[S['timestamp'] == t]["v5d"].values[0])
	vol5m=S.loc[S['timestamp'] == t]["v5m"].values[0]
	vol5s=S.loc[S['timestamp'] == t]["v5s"].values[0]

	vol30=literal_eval(S.loc[S['timestamp'] == t]["v30d"].values[0])
	vol30m=S.loc[S['timestamp'] == t]["v30d"].values[0]
	vol30s=S.loc[S['timestamp'] == t]["v30s"].values[0]

	roc=literal_eval(S.loc[S['timestamp'] == t]["rocd"].values[0])
	rocm=S.loc[S['timestamp'] == t]["rocm"].values[0]
	rocs=S.loc[S['timestamp'] == t]["rocs"].values[0]

	roc5=literal_eval(S.loc[S['timestamp'] == t]["roc5d"].values[0])
	roc5m=S.loc[S['timestamp'] == t]["roc5m"].values[0]
	roc5s=S.loc[S['timestamp'] == t]["roc5s"].values[0]

	roc30=literal_eval(S.loc[S['timestamp'] == t]["roc30d"].values[0])
	roc30m=S.loc[S['timestamp'] == t]["roc30m"].values[0]
	roc30s=S.loc[S['timestamp'] == t]["roc30s"].values[0]


	r=literal_eval(S.loc[S['timestamp'] == t]["rd"].values[0])
	rm=S.loc[S['timestamp'] == t]["rm"].values[0]
	rs=S.loc[S['timestamp'] == t]["rs"].values[0]

	r5=literal_eval(S.loc[S['timestamp'] == t]["r5d"].values[0])
	r5m=S.loc[S['timestamp'] == t]["r5m"].values[0]
	r5s=S.loc[S['timestamp'] == t]["r5s"].values[0]

	r30=literal_eval(S.loc[S['timestamp'] == t]["r30d"].values[0])
	r30m=S.loc[S['timestamp'] == t]["r30m"].values[0]
	r30s=S.loc[S['timestamp'] == t]["r30s"].values[0]


	#vol1 = np.array(vol1)

	vol1 = np.array(vol1)/1000
	vol5 = np.array(vol5)/1000
	vol30 = np.array(vol30)/1000

	i = 0
	if s_v1!=0:
		plot[i]["v1"].clear()
		plot[i]["v1"].set_title("Volume Past 1 minute",fontsize=8)
		plot[i]["v1"].boxplot(vol1, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["v1"],vol1m,vol1s,s_v1)
	#plot[i]["v1"].axvline(vol1[len(vol1)//2],c="r",linewidth=6 ,label='Current Position')
	#v1.set_xlabel("units: 1000 shares")

	if s_v5!=0:
		plot[i]["v5"].clear()
		plot[i]["v5"].set_title("Volume Past 5 minute",fontsize=8)
		plot[i]["v5"].boxplot(vol5, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["v5"],vol5m,vol5s,s_v5)
	#plot[i]["v5"].axvline(vol5[len(vol5)//2],c="r",linewidth=6 ,label='Current Position')

	if s_v30!=0:
		plot[i]["v30"].clear()
		plot[i]["v30"].set_title("Volume Past 30 minute",fontsize=8)
		plot[i]["v30"].boxplot(vol30, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["v30"],vol30m,vol30s,s_v30)
	#avline(plot[i]["v1"],5,6,10)
	#plot[i]["v30"].axvline(vol30[len(vol30)//2],c="r",linewidth=6 ,label='Current Position')

	if s_r1!= 0:
		plot[i]["r_"].clear()
		plot[i]["r_"].set_title("Range Past 1 minute",fontsize=8)
		plot[i]["r_"].boxplot(r, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["r_"],rm,rs,s_r1)
		#plot[i]["r_"].axvline(r[len(r)//2],c="r",linewidth=6 ,label='Current Position')
	if s_r5!= 0:
		plot[i]["r5_"].clear()
		plot[i]["r5_"].set_title("Range Past 5 minute",fontsize=8)
		plot[i]["r5_"].boxplot(r5, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["r5_"],r5m,r5s,s_r5)
		#plot[i]["r5_"].axvline(r5[len(r5)//2],c="r",linewidth=6 ,label='Current Position')

	if s_r30!= 0:
		plot[i]["r30_"].clear()	
		plot[i]["r30_"].set_title("Range Past 30 minute",fontsize=8)
		plot[i]["r30_"].boxplot(r30, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["r30_"],r30m,r30s,s_r30)
		#plot[i]["r30_"].axvline(r30[len(r30)//2],c="r",linewidth=6 ,label='Current Position')

	if s_roc!=0:
		plot[i]["roc_"].clear()
		plot[i]["roc_"].set_title("RoC Past 1 minute",fontsize=8)
		plot[i]["roc_"].boxplot(roc, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["roc_"],rocm,rocs,s_roc)
		#plot[i]["roc_"].axvline(roc[len(roc)//2],c="r",linewidth=6 ,label='Current Position')
	if s_roc5!=0:
		plot[i]["roc5_"].clear()
		plot[i]["roc5_"].set_title("RoC Past 5 minute",fontsize=8)
		plot[i]["roc5_"].boxplot(roc5, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["roc5_"],roc5m,roc5s,s_roc5)
		#plots["roc5_"].axvline(roc5[len(roc5)//2],c="r",linewidth=6 ,label='Current Position')
	if s_roc30!=0:
		plot[i]["roc30_"].clear()
		plot[i]["roc30_"].set_title("RoC Past 30 minute",fontsize=8)
		plot[i]["roc30_"].boxplot(roc30, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["roc30_"],roc30m,roc5m,s_roc30)




	#get values 
	with lock:
		s_v1=d.minute_volume_value[symbols[1]]/1000
		s_v5=d.minute_volume5_value[symbols[1]]/1000
		s_v30=d.minute_volume30_value[symbols[1]]/1000
		s_r1=d.minute_range_value[symbols[1]]
		s_r5=d.minute_range5_value[symbols[1]]
		s_r30=d.minute_range30_value[symbols[1]]
		s_roc=d.minute_roc_value[symbols[1]]
		s_roc5=d.minute_roc5_value[symbols[1]]
		s_roc30= d.minute_roc30_value[symbols[1]]

	print("Value check QQQ:\n",s_v1,s_v5,s_v30,"\n",s_r1,s_r5,s_r30,"\n",s_roc,s_roc5,s_roc30)
	
	vol1=literal_eval(Q.loc[Q['timestamp'] == t]["v1d"].values[0])
	vol1m=Q.loc[Q['timestamp'] == t]["v1m"].values[0]

	vol1s=Q.loc[Q['timestamp'] == t]["v1s"].values[0]

	vol5=literal_eval(Q.loc[Q['timestamp'] == t]["v5d"].values[0])
	vol5m=Q.loc[Q['timestamp'] == t]["v5m"].values[0]
	vol5s=Q.loc[Q['timestamp'] == t]["v5s"].values[0]

	vol30=literal_eval(Q.loc[Q['timestamp'] == t]["v30d"].values[0])
	vol30m=Q.loc[Q['timestamp'] == t]["v30d"].values[0]
	vol30s=Q.loc[Q['timestamp'] == t]["v30s"].values[0]

	roc=literal_eval(Q.loc[Q['timestamp'] == t]["rocd"].values[0])
	rocm=Q.loc[Q['timestamp'] == t]["rocm"].values[0]
	rocs=Q.loc[Q['timestamp'] == t]["rocs"].values[0]

	roc5=literal_eval(Q.loc[Q['timestamp'] == t]["roc5d"].values[0])
	roc5m=Q.loc[Q['timestamp'] == t]["roc5m"].values[0]
	roc5s=Q.loc[Q['timestamp'] == t]["roc5s"].values[0]

	roc30=literal_eval(Q.loc[Q['timestamp'] == t]["roc30d"].values[0])
	roc30m=Q.loc[Q['timestamp'] == t]["roc30m"].values[0]
	roc30s=Q.loc[Q['timestamp'] == t]["roc30s"].values[0]


	r=literal_eval(Q.loc[Q['timestamp'] == t]["rd"].values[0])
	rm=Q.loc[Q['timestamp'] == t]["rm"].values[0]
	rs=Q.loc[Q['timestamp'] == t]["rs"].values[0]

	r5=literal_eval(Q.loc[Q['timestamp'] == t]["r5d"].values[0])
	r5m=Q.loc[Q['timestamp'] == t]["r5m"].values[0]
	r5s=Q.loc[Q['timestamp'] == t]["r5s"].values[0]

	r30=literal_eval(Q.loc[Q['timestamp'] == t]["r30d"].values[0])
	r30m=Q.loc[Q['timestamp'] == t]["r30m"].values[0]
	r30s=Q.loc[Q['timestamp'] == t]["r30s"].values[0]


	#vol1 = np.array(vol1)

	vol1 = np.array(vol1)/1000
	vol5 = np.array(vol5)/1000
	vol30 = np.array(vol30)/1000

	i = 1
	if s_v1!=0:
		plot[i]["v1"].clear()
		plot[i]["v1"].set_title("Volume Past 1 minute",fontsize=8)
		plot[i]["v1"].boxplot(vol1, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["v1"],vol1m,vol1s,s_v1)
	#plot[i]["v1"].axvline(vol1[len(vol1)//2],c="r",linewidth=6 ,label='Current Position')
	#v1.set_xlabel("units: 1000 shares")

	if s_v5!=0:
		plot[i]["v5"].clear()
		plot[i]["v5"].set_title("Volume Past 5 minute",fontsize=8)
		plot[i]["v5"].boxplot(vol5, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["v5"],vol5m,vol5s,s_v5)
	#plot[i]["v5"].axvline(vol5[len(vol5)//2],c="r",linewidth=6 ,label='Current Position')

	if s_v30!=0:
		plot[i]["v30"].clear()
		plot[i]["v30"].set_title("Volume Past 30 minute",fontsize=8)
		plot[i]["v30"].boxplot(vol30, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["v30"],vol30m,vol30s,s_v30)
	#avline(plot[i]["v1"],5,6,10)
	#plot[i]["v30"].axvline(vol30[len(vol30)//2],c="r",linewidth=6 ,label='Current Position')

	if s_r1!= 0:
		plot[i]["r_"].clear()
		plot[i]["r_"].set_title("Range Past 1 minute",fontsize=8)
		plot[i]["r_"].boxplot(r, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["r_"],rm,rs,s_r1)
		#plot[i]["r_"].axvline(r[len(r)//2],c="r",linewidth=6 ,label='Current Position')
	if s_r5!= 0:
		plot[i]["r5_"].clear()
		plot[i]["r5_"].set_title("Range Past 5 minute",fontsize=8)
		plot[i]["r5_"].boxplot(r5, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["r5_"],r5m,r5s,s_r5)
		#plot[i]["r5_"].axvline(r5[len(r5)//2],c="r",linewidth=6 ,label='Current Position')

	if s_r30!= 0:
		plot[i]["r30_"].clear()	
		plot[i]["r30_"].set_title("Range Past 30 minute",fontsize=8)
		plot[i]["r30_"].boxplot(r30, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["r30_"],r30m,r30s,s_r30)
		#plot[i]["r30_"].axvline(r30[len(r30)//2],c="r",linewidth=6 ,label='Current Position')

	if s_roc!=0:
		plot[i]["roc_"].clear()
		plot[i]["roc_"].set_title("RoC Past 1 minute",fontsize=8)
		plot[i]["roc_"].boxplot(roc, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["roc_"],rocm,rocs,s_roc)
		#plot[i]["roc_"].axvline(roc[len(roc)//2],c="r",linewidth=6 ,label='Current Position')
	if s_roc5!=0:
		plot[i]["roc5_"].clear()
		plot[i]["roc5_"].set_title("RoC Past 5 minute",fontsize=8)
		plot[i]["roc5_"].boxplot(roc5, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["roc5_"],roc5m,roc5s,s_roc5)
		#plots["roc5_"].axvline(roc5[len(roc5)//2],c="r",linewidth=6 ,label='Current Position')
	if s_roc30!=0:
		plot[i]["roc30_"].clear()
		plot[i]["roc30_"].set_title("RoC Past 30 minute",fontsize=8)
		plot[i]["roc30_"].boxplot(roc30, flierprops=outlier,vert=False, whis=1)
		avline(plot[i]["roc30_"],roc30m,roc5m,s_roc30)
	# vol1=literal_eval(Q.loc[Q['timestamp'] == t]["v1d"].values[0])
	# vol5=literal_eval(Q.loc[Q['timestamp'] == t]["v5d"].values[0])
	# vol30=literal_eval(Q.loc[Q['timestamp'] == t]["v30d"].values[0])

	# roc=literal_eval(Q.loc[Q['timestamp'] == t]["rocd"].values[0])
	# roc5=literal_eval(Q.loc[Q['timestamp'] == t]["roc5d"].values[0])
	# roc30=literal_eval(Q.loc[Q['timestamp'] == t]["roc30d"].values[0])

	# r=literal_eval(Q.loc[Q['timestamp'] == t]["rd"].values[0])
	# r5=literal_eval(Q.loc[Q['timestamp'] == t]["r5d"].values[0])
	# r30=literal_eval(Q.loc[Q['timestamp'] == t]["r30d"].values[0])

	# #vol1 = np.array(vol1)

	# vol1 = np.array(vol1)/1000
	# vol5 = np.array(vol5)/1000
	# vol30 = np.array(vol30)/1000

	# i = 1
	# plot[i]["v1"].clear()
	# plot[i]["v1"].set_title("Volume Past 1 minute",fontsize=8)
	# plot[i]["v1"].boxplot(vol1, flierprops=outlier,vert=False, whis=1)
	# avline(plot[i]["v1"],5,6,10)
	# #plot[i]["v1"].axvline(vol1[len(vol1)//2],c="r",linewidth=6 ,label='Current Position')
	# #v1.set_xlabel("units: 1000 shares")

	# plot[i]["v5"].clear()
	# plot[i]["v5"].set_title("Volume Past 5 minute",fontsize=8)
	# plot[i]["v5"].boxplot(vol5, flierprops=outlier,vert=False, whis=1)
	# #plot[i]["v5"].axvline(vol5[len(vol5)//2],c="r",linewidth=6 ,label='Current Position')

	# plot[i]["v30"].clear()
	# plot[i]["v30"].set_title("Volume Past 30 minute",fontsize=8)
	# plot[i]["v30"].boxplot(vol30, flierprops=outlier,vert=False, whis=1)
	# #plot[i]["v30"].axvline(vol30[len(vol30)//2],c="r",linewidth=6 ,label='Current Position')

	# plot[i]["r_"].clear()
	# plot[i]["r_"].set_title("Range Past 1 minute",fontsize=8)
	# plot[i]["r_"].boxplot(r, flierprops=outlier,vert=False, whis=1)
	# #plot[i]["r_"].axvline(r[len(r)//2],c="r",linewidth=6 ,label='Current Position')

	# plot[i]["r5_"].clear()
	# plot[i]["r5_"].set_title("Range Past 5 minute",fontsize=8)
	# plot[i]["r5_"].boxplot(r5, flierprops=outlier,vert=False, whis=1)
	# #plot[i]["r5_"].axvline(r5[len(r5)//2],c="r",linewidth=6 ,label='Current Position')


	# plot[i]["r30_"].clear()	
	# plot[i]["r30_"].set_title("Range Past 30 minute",fontsize=8)
	# plot[i]["r30_"].boxplot(r30, flierprops=outlier,vert=False, whis=1)
	# #plot[i]["r30_"].axvline(r30[len(r30)//2],c="r",linewidth=6 ,label='Current Position')

	# plot[i]["roc_"].clear()
	# plot[i]["roc_"].set_title("RoC Past 1 minute",fontsize=8)
	# plot[i]["roc_"].boxplot(roc, flierprops=outlier,vert=False, whis=1)
	# #plot[i]["roc_"].axvline(roc[len(roc)//2],c="r",linewidth=6 ,label='Current Position')

	# plot[i]["roc5_"].clear()
	# plot[i]["roc5_"].set_title("RoC Past 5 minute",fontsize=8)
	# plot[i]["roc5_"].boxplot(roc5, flierprops=outlier,vert=False, whis=1)
	# #plots["roc5_"].axvline(roc5[len(roc5)//2],c="r",linewidth=6 ,label='Current Position')

	# plot[i]["roc30_"].clear()
	# plot[i]["roc30_"].set_title("RoC Past 30 minute",fontsize=8)
	# plot[i]["roc30_"].boxplot(roc30, flierprops=outlier,vert=False, whis=1)



figs = UI_init(["S","Q"], "b")

def hello():
	print("HI")

def main(d,symbols,lock):	
	print("UI start")
	ani = FuncAnimation(figs,update,fargs=(d,symbols,lock),interval=2000)
	plt.tight_layout()
	plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.45, hspace= 0.45)
	plt.show()















if __name__ == "__main__":  
	print("process") 
	p = multiprocessing.Process(target=main, args=(histo, symbols, lock))
	#p = multiprocessing.Process(target=hello, args=(),daemon=True),daemon=True
	p.start()

test.start()
while True:
	i =0