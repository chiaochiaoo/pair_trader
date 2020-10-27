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

		self.intra_spread = []
		self.intra_spread_MA5 = []
		self.intra_spread_MA15 = []

		self.roc_1 = 0
		self.roc_15 = 0
		self.roc_30 = 0

		self.roc_1_list=[]
		self.roc_5_list=[]
		self.roc_15_list=[]

		self.cors_5 = []
		self.cors_15 = []

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


	def start_function(self):

		print("Console (PT): Pair trading moudule begins. ")
		super().tos_start()

		interval = self.interval

		x = 12
		while True:

			current_time = time.time()

			self.aggregate_data()

			lag = (time.time() - current_time)
			sleep = self.interval
			if interval*1000-lag> 0 : sleep = (interval*1000-lag)/1000

			if x %12 ==0:
				print("\nConsole (PT): Processing for ",round(lag*1000,2),"ms , Sleep for",round(sleep,5),"s \n")

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

		spread = self.cur_percentage_change[a] - self.cur_percentage_change[b]

		spread_ma5 = (sum(self.intra_spread[-300:]) + spread)/(len(self.intra_spread[-300:])+1) 
		spread_ma15 = (sum(self.intra_spread[-1500:]) + spread)/(len(self.intra_spread[-1500:])+1)

		#What if not that time yet.


		if len(self.intra_spread)>60:
			self.roc_1 = self.intra_spread[-60] - spread

		if len(self.intra_spread)>300:
			self.roc_5 = self.intra_spread[-300] - spread

		if len(self.intra_spread)>1500:
			self.roc_15 = self.intra_spread[-1500] - spread



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
			self.intra_spread.append(spread)
			self.intra_spread_MA5.append(spread_ma5)
			self.intra_spread_MA15.append(spread_ma15)

			self.roc_1_list.append(self.roc_1)
			self.roc_5_list.append(self.roc_5)
			self.roc_15_list.append(self.roc_15)

			self.cors_5.append(cor_5)
			self.cors_15.append(cor_15)

		#print("Legnth check",len(self.cur_time),len(self.intra_spread),len(self.roc),len(self.cors_10),len(self.vol_ratio_15))

	# integrated graphing conponent. 
	#def graph(self):


if len(sys.argv) ==1:
	symbols = ["SPY.AM","QQQ.NQ"]
	readlock = threading.Lock()
	test = Pair_trading_processor(symbols,1,TESTMODE,readlock)
	test.start()

else:
	symbols = sys.argv[1].split(",")
	readlock = threading.Lock()

	test = Pair_trading_processor(symbols,1,REALMODE,readlock)
	test.start()

	#test = Pair_trading_processor(symbols,3,TESTMODE,readlock)
















































































































#plt.show()


