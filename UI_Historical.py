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
import threading
import datetime
from ast import literal_eval

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

#main()

# v1 = f.add_subplot(341)
# v5 = f.add_subplot(342)
# v30 = f.add_subplot(343)
# r_ = f.add_subplot(345)
# r5_ = f.add_subplot(346)
# r30_ = f.add_subplot(347)

# roc_ = f.add_subplot(349)
# roc5_ = f.add_subplot(3,4,10)
# roc30_ = f.add_subplot(3,4,11)

# v1.set_title("Volume Past 1 minute",fontsize=8)
# v1.boxplot(vol1, flierprops=outlier,vert=False, whis=1)
# v1.axvline(vol1[len(vol1)//2],c="r",linewidth=6 ,label='Current Position')
# #v1.set_xlabel("units: 1000 shares")

# v5.set_title("Volume Past 5 minute",fontsize=8)
# v5.boxplot(vol5, flierprops=outlier,vert=False, whis=1)
# v5.axvline(vol5[len(vol5)//2],c="r",linewidth=6 ,label='Current Position')


# v30.set_title("Volume Past 30 minute",fontsize=8)
# v30.boxplot(vol30, flierprops=outlier,vert=False, whis=1)
# v30.axvline(vol30[len(vol30)//2],c="r",linewidth=6 ,label='Current Position')




# r_.set_title("Range Past 1 minute",fontsize=8)
# r_.boxplot(r, flierprops=outlier,vert=False, whis=1)
# r_.axvline(r[len(r)//2],c="r",linewidth=6 ,label='Current Position')


# r5_.set_title("Range Past 5 minute",fontsize=8)
# r5_.boxplot(r5, flierprops=outlier,vert=False, whis=1)
# r5_.axvline(r5[len(r5)//2],c="r",linewidth=6 ,label='Current Position')



# r30_.set_title("Range Past 30 minute",fontsize=8)
# r30_.boxplot(r30, flierprops=outlier,vert=False, whis=1)
# r30_.axvline(r30[len(r30)//2],c="r",linewidth=6 ,label='Current Position')


# roc_.set_title("RoC Past 1 minute",fontsize=8)
# roc_.boxplot(roc, flierprops=outlier,vert=False, whis=1)
# roc_.axvline(roc[len(roc)//2],c="r",linewidth=6 ,label='Current Position')


# roc5_.set_title("RoC Past 5 minute",fontsize=8)
# roc5_.boxplot(roc5, flierprops=outlier,vert=False, whis=1)
# #roc5_.axvline(roc5[len(roc5)//2],c="r",linewidth=6 ,label='Current Position')



# roc30_.set_title("RoC Past 30 minute",fontsize=8)
# roc30_.boxplot(roc30, flierprops=outlier,vert=False, whis=1)


#roc30_.axvline(roc30[len(roc30)//2],c="r",linewidth=6 ,label='Current Position')
	
# plt.style.use("seaborn-darkgrid")
# f = plt.figure(1,figsize=(10,10))
# f.canvas.set_window_title('HISTORICAL COMPARISON')


# vlow="Very low"
# low="Low"
# avg="Average"
# high="High"
# vhigh="Very High"
# dot = "•"

# text1 = "Past One Minute Evaluation:                                                                            \n"
# text2 = "Next Minute:                                                                         \n"

# info1 = []
# info1.append("• Volume in past 1 minute: High than Historical Average")
# info1.append("• Volume in past 5 minute: High than Historical Average")
# info1.append("• Volume in past 30 minute: Very High than Historical Average")
# info1.append("• Range in past 5 minute: Very High than Historical Average")
# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# #bbox=props,
# plt.text(0.71, 0.8, text1+listToString(info1), fontsize=10, transform=plt.gcf().transFigure, verticalalignment='center')

# info2 = []
# info2.append("• Range in next 1 minute: Very High Historically")
# info2.append("• Range in next 5 minute: Very High Historically")
# info2.append("• Rate of Change in next 5 minutes: High Historically")

# plt.text(0.71, 0.6, text2+listToString(info2), fontsize=10, transform=plt.gcf().transFigure, verticalalignment='center')
#plt.subplots_adjust(bottom = 0.15) 

# f2 = plt.figure(2,figsize=(10,10))
# f2.canvas.set_window_title('Evaluation & Alerts')










#SENSORY OVERLOAD 

# plt.style.use("seaborn-darkgrid")
# f = plt.figure(1,figsize=(10,10))
# f.canvas.set_window_title('HISTORICAL COMPARISON')

# outlier = dict(markerfacecolor='black', marker='o')
# time = 0
# vol1=[163559, 97594, 103898, 86110, 167141, 98180, 230912, 227648, 117170, 72966, 113922, 78094, 76669, 147990, 116530, 159217, 116928, 193061, 238097, 135130, 135310, 269112, 240802, 189675, 314157, 454354, 309601, 228671, 214194, 137873, 189141, 130205, 377212, 223837, 312861, 207699, 86134, 394293, 208543, 178920, 81019]
# vol5=[1685880, 1217755, 856075, 815803, 1406273, 801215, 1379215, 1471851, 1068518, 901913, 913112, 786357, 752979, 1624522, 1332576, 1212148, 1031213, 1058720, 1431932, 946426, 1163385, 1653090, 1741324, 1718471, 2560033, 3269008, 2296114, 1172260, 1335430, 1052259, 1227858, 999180, 2490608, 3072112, 2659605, 1491069, 984457, 2339353, 1612260, 1844700, 929584]
# vol30=[1920581, 1364821, 997351, 935296, 1644281, 882354, 1543746, 1666407, 1242215, 1075572, 1014676, 903214, 852568, 2371914, 1820431, 1312104, 1218759, 1420741, 2491720, 1030837, 1393134, 1984474, 2002438, 2035963, 3121851, 3730600, 2921881, 1432588, 1502843, 1461244, 1539989, 1079180, 3071093, 3520011, 3350221, 1642613, 1078089, 2713218, 1971473, 1988776, 1113973]

# volacc=[2829397, 2219298, 1733506, 2231213, 3407634, 1312243, 2246864, 2752826, 1850836, 1884088, 1620091, 1487211, 1217854, 3099456, 3177595, 2052529, 1563282, 1857510, 3274480, 50135329, 2107459, 2622479, 2575015, 3747931, 5431928, 5553474, 5117667, 2680358, 2289605, 2123266, 2439076, 1844801, 4887319, 4103212, 5310118, 2715190, 1844168, 4862316, 3281193, 2781875, 1855834]

# roc=[-0.160000000000025, 0.040000000000020464, -0.0999999999999659, -0.0999999999999659, 0.06999999999999318, 0.13999999999998636, -0.160000000000025, -0.06999999999999318, -0.17999999999994998, -0.06999999999999318, 0.040000000000020464, -0.05000000000001137, 0.03000000000002956, 0.22999999999996135, 0.03999999999996362, -0.13999999999998636, -0.060000000000002274, 0.11000000000001364, 0.18000000000000682, 0.25, -0.160000000000025, 0.30000000000001137, 0.08999999999997499, -0.6000000000000227, -0.12000000000000455, 0.3299999999999841, 0.17000000000001592, 0.30000000000001137, -0.45999999999997954, -0.15999999999996817, -0.0999999999999659, -0.17000000000001592, 0.040000000000020464, -0.060000000000002274, -0.75, -0.28000000000002956, -0.016999999999995907, -0.44999999999998863, 0.060000000000002274, 0.07999999999998408, -0.045000000000015916]
# roc5=[-0.26000000000004775, 0.6100000000000136, -0.2699999999999818, 0.30000000000001137, 0.3199999999999932, 0.13999999999998636, -0.18999999999999773, 0.4700000000000273, 0.020000000000038654, -0.3599999999999568, 0.03000000000002956, 0.160000000000025, -0.20999999999997954, 0.47999999999996135, 0.18999999999999773, -0.30999999999994543, -0.4900000000000091, -0.19999999999998863, -0.5500000000000114, -0.5999999999999659, -0.13999999999998636, -0.5999999999999659, -0.8000000000000114, -0.21000000000003638, 0.9599999999999795, -0.7900000000000205, -0.12999999999999545, 0.4300000000000068, -0.7999999999999545, -0.3199999999999932, 0.12999999999999545, -0.14999999999997726, 0.09000000000003183, -0.8799999999999955, -0.3199999999999932, -0.020000000000038654, -0.17699999999996407, -0.9399999999999977, 0.18999999999999773, 0.44999999999998863, -0.09500000000002728]
# roc30=[-0.37000000000000455, 0.7200000000000273, -0.2899999999999636, 0.2300000000000182, 0.15999999999996817, 0.30000000000001137, -0.5, 0.22000000000002728, -0.3499999999999659, -0.2899999999999636, 0.17000000000001592, -0.12999999999999545, 0.14999999999997726, 0.009999999999990905, 1.4300000000000068, -0.4199999999999591, -1.0400000000000205, 0.03999999999996362, 0.5300000000000296, -0.5999999999999659, -0.160000000000025, -0.3499999999999659, -0.660000000000025, -0.4399999999999977, 0.46999999999997044, -1.1200000000000045, 0.7800000000000296, 1.1399999999999864, -0.7599999999999909, 0.040000000000020464, 0.0, -0.6299999999999955, 0.44999999999998863, -1.009999999999991, -0.5999999999999659, 0.45999999999997954, -0.14699999999999136, -0.01999999999998181, -0.12000000000000455, 0.24979999999999336, -0.20500000000004093]

# r=[0.25, 0.15999999999996817, 0.16999999999995907, 0.2599999999999909, 0.14999999999997726, 0.16999999999995907, 0.2300000000000182, 0.2400000000000091, 0.2300000000000182, 0.15999999999996817, 0.12000000000000455, 0.1300000000000523, 0.12999999999999545, 0.2599999999999909, 0.1500000000000341, 0.13999999999998636, 0.18000000000000682, 0.20999999999997954, 0.4399999999999977, 0.40999999999996817, 0.18999999999999773, 0.3199999999999932, 0.25, 0.6899999999999977, 0.28000000000002956, 0.5600000000000023, 0.35000000000002274, 0.37000000000000455, 0.4900000000000091, 0.2599999999999909, 0.20999999999997954, 0.25, 0.25, 0.21500000000003183, 1.0299999999999727, 0.37520000000000664, 0.20199999999999818, 0.6499999999999773, 0.37000000000000455, 0.160000000000025, 0.18999999999999773]
# r5=[0.5199999999999818, 0.7699999999999818, 0.2699999999999818, 0.5400000000000205, 0.6700000000000159, 0.25, 0.5500000000000114, 0.6700000000000159, 0.46999999999997044, 0.6499999999999773, 0.2899999999999636, 0.2799999999999727, 0.37999999999999545, 0.6499999999999773, 0.25, 0.39999999999997726, 0.6599999999999682, 0.5400000000000205, 0.8700000000000045, 0.9699999999999704, 0.40999999999996817, 0.9900000000000091, 0.9499999999999886, 0.7799999999999727, 2.1399999999999864, 1.2999999999999545, 0.5099999999999909, 1.009999999999991, 1.5, 0.7699999999999818, 0.4399999999999977, 0.3599999999999568, 0.7900000000000205, 0.8899999999999864, 1.3199999999999932, 0.7730000000000246, 0.3849999999999909, 1.5600000000000023, 0.6100000000000136, 0.37000000000000455, 0.4500000000000455]
# r30=[0.5799999999999841, 0.8600000000000136, 0.45999999999997954, 0.5400000000000205, 0.7299999999999613, 0.5600000000000023, 0.5600000000000023, 0.75, 0.5299999999999727, 0.6499999999999773, 0.2899999999999636, 0.5, 0.44999999999998863, 0.6700000000000159, 1.3199999999999932, 0.5, 1.1099999999999568, 0.7200000000000273, 2.1499999999999773, 1.0699999999999932, 0.4399999999999977, 0.9900000000000091, 1.170000000000016, 0.7799999999999727, 2.1399999999999864, 1.9499999999999886, 1.0500000000000114, 1.330000000000041, 1.5, 0.7699999999999818, 0.4399999999999977, 0.7299999999999613, 1.1899999999999977, 1.5499999999999545, 1.329999999999984, 0.9399999999999977, 0.3849999999999909, 1.920000000000016, 0.8400000000000318, 0.6000000000000227, 0.6300000000000523]

# vol1 = np.array(vol1)/1000
# vol5 = np.array(vol5)/1000
# vol30 = np.array(vol30)/1000

# roc=np.array(roc)
# roc5=np.array(roc5)
# roc30=np.array(roc30)


# v1 = f.add_subplot(361)
# v1.set_title("Volume 1 minute",fontsize=8)
# v1.boxplot(vol1, flierprops=outlier,vert=False, whis=1)
# v1.axvline(vol1[len(vol1)//2],c="r",linewidth=6 ,label='Current Position')
# #v1.set_xlabel("units: 1000 shares")

# v5 = f.add_subplot(362)
# v5.set_title("Volume 5 minute",fontsize=8)
# v5.boxplot(vol5, flierprops=outlier,vert=False, whis=1)
# v5.axvline(vol5[len(vol5)//2],c="r",linewidth=6 ,label='Current Position')

# v30 = f.add_subplot(363)
# v30.set_title("Volume 30 minute",fontsize=8)
# v30.boxplot(vol30, flierprops=outlier,vert=False, whis=1)
# v30.axvline(vol30[len(vol30)//2],c="r",linewidth=6 ,label='Current Position')

# v1 = f.add_subplot(364)
# v1.set_title("Historically Volume next 1 minute",fontsize=8)
# v1.boxplot(vol1+22, flierprops=outlier,vert=False, whis=1)

# #v1.set_xlabel("units: 1000 shares")

# v5 = f.add_subplot(365)
# v5.set_title("Historically Volume next 5 minute",fontsize=8)
# v5.boxplot(vol5+35, flierprops=outlier,vert=False, whis=1)
 

# v30 = f.add_subplot(366)
# v30.set_title("Historically Volume next 30 minute",fontsize=8)
# v30.boxplot(vol30+92, flierprops=outlier,vert=False, whis=1)
 


# r_ = f.add_subplot(367)
# r_.set_title("Range 1 minute",fontsize=8)
# r_.boxplot(r, flierprops=outlier,vert=False, whis=1)
# r_.axvline(r[len(r)//2],c="r",linewidth=6 ,label='Current Position')

# r5_ = f.add_subplot(368)
# r5_.set_title("Range 5 minute",fontsize=8)
# r5_.boxplot(r5, flierprops=outlier,vert=False, whis=1)
# r5_.axvline(r5[len(r5)//2],c="r",linewidth=6 ,label='Current Position')


# r30_ = f.add_subplot(369)
# r30_.set_title("Range 30 minute",fontsize=8)
# r30_.boxplot(r30, flierprops=outlier,vert=False, whis=1)
# r30_.axvline(r30[len(r30)//2],c="r",linewidth=6 ,label='Current Position')


# r_ = f.add_subplot(3,6,10)
# r_.set_title("Hitorically Range next 1 minute",fontsize=8)
# r_.boxplot(r, flierprops=outlier,vert=False, whis=1)


# r5_ = f.add_subplot(3,6,11) 
# r5_.set_title("Hitorically Range next 5 minute",fontsize=8)
# r5_.boxplot(r5, flierprops=outlier,vert=False, whis=1)



# r30_ = f.add_subplot(3,6,12)
# r30_.set_title("Hitorically Range next 30 minute",fontsize=8)
# r30_.boxplot(r30, flierprops=outlier,vert=False, whis=1)



# roc_ = f.add_subplot(3,6,13)
# roc_.set_title("RoC 1 minute",fontsize=8)
# roc_.boxplot(roc, flierprops=outlier,vert=False, whis=1)
# roc_.axvline(roc[len(roc)-7//2],c="r",linewidth=6 ,label='Current Position')

# roc5_ = f.add_subplot(3,6,14)
# roc5_.set_title("RoC 5 minute",fontsize=8)
# roc5_.boxplot(roc5, flierprops=outlier,vert=False, whis=1)
# roc5_.axvline(roc5[len(roc5)-3//2],c="r",linewidth=6 ,label='Current Position')


# roc30_ = f.add_subplot(3,6,15)
# roc30_.set_title("RoC 30 minute",fontsize=8)
# roc30_.boxplot(roc30, flierprops=outlier,vert=False, whis=1)
# roc30_.axvline(roc30[len(roc30)-4//2],c="r",linewidth=6 ,label='Current Position')


# roc_ = f.add_subplot(3,6,16)
# roc_.set_title("Hitorically RoC next 1 minute",fontsize=8)
# roc_.boxplot(roc, flierprops=outlier,vert=False, whis=1)


# roc5_ = f.add_subplot(3,6,17)
# roc5_.set_title("Hitorically RoC next 5 minute",fontsize=8)
# roc5_.boxplot(roc5, flierprops=outlier,vert=False, whis=1)



# roc30_ = f.add_subplot(3,6,18)
# roc30_.set_title("Hitorically RoC next 30 minute",fontsize=8)
# roc30_.boxplot(roc30+0.2, flierprops=outlier,vert=False, whis=1)




# # vlow="Very low"
# # low="Low"
# # avg="Average"
# # high="High"
# # vhigh="Very High"
# # dot = "•"

# text1 = "Alerts:                                                                            \n"

# info1 = []

# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# #bbox=props,
# plt.text(0.1, 0.95, text1+listToString(info1), fontsize=10, transform=plt.gcf().transFigure,bbox=props, verticalalignment='center')

