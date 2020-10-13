import TOS
import threading
import time
import pandas as pd
import numpy as np
import datetime
import Functions as chiao

import Database

# import UI_Historical
# import multiprocessing
#cur_minute = pd.to_datetime(cur_time,format='%H:%M:%S')
####
# from matplotlib.animation import FuncAnimation
# from matplotlib.dates import DateFormatter
# import matplotlib.dates as mdates
# import matplotlib.pyplot as plt 
############### TEST CODE ##########################

TESTMODE = False
REALMODE = True



class Data_processor:

	def __init__(self,symbols,interval,tos_mode,readlock):


		self.symbols = symbols
		self.tosmode = tos_mode
		self.interval = interval

		self.cur_time = []
		self.cur_minute_list = []
		self.cur_minute = 0
		self.readlock = readlock

		# minute counter is in how many loops it will become one minute. 
		# self.minute_counter = interval
		# if tos_mode:
		self.minute_counter = 60//interval 
		self.aggregate_counter = 0

		# This is the bin value, gather, and clean after every interval. Used with TOS. 

		self.binlock = threading.Lock()
		self.tos_registration = False
		self.price ={}
		self.volume = {}

		for i in symbols:
			self.price[i] = []
			self.volume[i] = []


		self.accumulated_volume = {}

		symbols_split =[i.split(".")[0] for i in symbols]

		volumes = Database.fetch_volume(symbols_split)
		index = 0
		for i in symbols:
			self.accumulated_volume[i] = volumes[index]
			index += 1 

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



		# A list of vallues contain vol1 ,vol5, vol30, volacc, range1,530, roc1,5,30
		self.minute_vals = {}
		for i in symbols:

			self.minute_vals[i] = [0,0,0,0,0,0,0,0,0,0]
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


		print("Console (DP): Synchronizing minutes")
		while self.tosmode == True:
			now = datetime.datetime.now()
			if (now.second>55) or (now.second<5):
				break


		now = datetime.datetime.now()
		t = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))

		print("Console (DP): Processing begins at",t)
		# with self.binlock:
		# 	for i in self.symbols:

		# 		print("Console (DP): Processing",i,"transaction counts:",len(self.price[i]),len(self.volume[i]))
		# 		self.price[i] = []
		# 		self.volume[i] = []

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

					#add this to the total bin
					self.accumulated_volume[i] += self.minute_volume_value[i]

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

					self.minute_vals[i] = [self.minute_volume_value[i],self.minute_volume5_value[i],self.minute_volume30_value[i],\
											self.minute_range_value[i],self.minute_range5_value[i],self.minute_range30_value[i],\
											self.minute_roc_value[i],self.minute_roc5_value[i],self.minute_roc30_value[i],self.accumulated_volume[i]]

					self.minute_vals[i] = [round(i,3) for i in self.minute_vals[i]]
					#self.minute_vals[i] = [5 for i in self.minute_vals[i]]
					now = datetime.datetime.now()
					t = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))
					print("\nConsole (DP): One Minute ",i,t, self.minute_vals[i],"\n")
					#print("Length check for 30:",len(self.minute_open_list[i]),self.minute_open_list[i])

					#print("Length: minute open close:",len(self.minute_open_list[i]),len(self.minute_close_list[i]))
					#print("Length: volume :",len(self.minute_volume_list[i]),)
					#print("Length: range high_ low:",len(self.minute_high_list[i]),len(self.minute_low_list[i]))



			#TODO
		#### WRITING BLOCK SAVE TO A CSV FILE ####################



####### USE.

# symbols = ["SPY.AM","QQQ.NQ"]
# readlock = threading.Lock()
# test = Data_processor(symbols,5,TESTMODE,readlock)
# test.start()

# class hist:
# 	def __init__(self):
# 		self.minute_volume_value = {}
# 		self.minute_volume5_value = {}
# 		self.minute_volume30_value = {}
# 		self.minute_range_value = {}
# 		self.minute_range5_value = {}
# 		self.minute_range30_value = {}
# 		self.minute_roc_value = {}
# 		self.minute_roc5_value = {}
# 		self.minute_roc30_value = {}

# 	def set_hist(self,d):

# 		self.minute_volume_value = d.minute_volume_value
# 		self.minute_volume5_value = d.minute_volume5_value
# 		self.minute_volume30_value = d.minute_volume30_value
# 		self.minute_range_value = d.minute_range_value
# 		self.minute_range5_value = d.minute_range5_value
# 		self.minute_range30_value = d.minute_range30_value
# 		self.minute_roc_value = d.minute_roc_value
# 		self.minute_roc5_value = d.minute_roc5_value
# 		self.minute_roc30_value = d.minute_roc30_value

# 		print("CHECK",self.minute_volume_value)

# histo = hist()

# test = Data_processor(symbols,5,TESTMODE,readlock,histo)

# lock = multiprocessing.Lock()



# q = Queue()
# p = Process(target=f, args=(q,))
# p.start()

#UI_Historical.main(histo, symbols,readlock)













































