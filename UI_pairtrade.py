import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as mticker
from matplotlib.widgets import TextBox
from matplotlib.widgets import Button
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import numpy as np
import Functions as chiao
import pandas as pd



def report(spy,qqq,sma,std):

	n = round(((spy-qqq)-sma)/std,2)

	text = ""
	if n >=0:
		text = "+" + str(n) + "STD away from the regression line"
	else:
		text = "-" + str(n) + "STD away from the regression line"

	return text


def equidate_ax(fig, ax, dates, fmt="%m-%d"):    
    N = len(dates)
    def format_date(index, pos):
        index = np.clip(int(index + 0.5), 0, N - 1)
        return dates[index].strftime(fmt)
    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_xlabel("dates")
    fig.autofmt_xdate()
############################################################################

GAP =pd.read_csv('data/SPYQQQpair.csv')

week = 960*5
month_dates = pd.to_datetime(GAP["timestamp"],format='%m/%d/%Y %H:%M')
month_GAP = GAP["price_gap"]
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

d=np.arange(len(week_dates))
d2=np.arange(len(d_dates))
newd = [len(d)]
newd2 = [len(d2)]
newGAP = [week_GAP[-1]]


############################################################################


plt.style.use("seaborn-darkgrid")
f = plt.figure(1,figsize=(8,10))
f.canvas.set_window_title('SPREAD MONITOR')


w_spread = f.add_subplot(511)

w_spread.set_title("Intraday Spread - Past one Week",fontsize=8)
w_spread.plot(d,week_GAP,"r",label="Spread")
w_spread.plot(d,w_SMA,"c",label="Spread SMA10")
w_spread.plot(d,w_regression_line,"b",label="Regression line",linewidth=1)
w_spread.fill_between(d, w_regression_line-2*w_std,w_regression_line+2*w_std,alpha=0.23,label="Price gap deviation zone")
w_spread.tick_params(axis='both', which='major', labelsize=8)
equidate_ax(f,w_spread,list(week_dates))


d_spread = f.add_subplot(512)

d_spread.set_title("Intraday Spread - Past one Day",fontsize=8)
d_spread.plot(d2,d_GAP,"r",label="Spread")
d_spread.plot(d2,d_SMA,"c",label="Spread SMobjectA10")
d_spread.plot(d2,d_regression_line,"b--",label="Regression line",linewidth=1)
d_spread.fill_between(d2, d_SMA-2*d_std,d_SMA+2*d_std,alpha=0.23,label="Price gap deviation zone")
d_spread.tick_params(axis='both', which='major', labelsize=8)


daily_spread = f.add_subplot(513)
daily_spread.set_title("Intraday Spread - Today",fontsize=8)
daily_spread.tick_params(axis='both', which='major', labelsize=8)


yrange = [i/10 +0. for i in range(0,11,2)]
yrange_cor = [round(i/10 +-1.,2) for i in range(0,21,2)]

vol15 = f.add_subplot(5,3,10)
vol15.set_title("Volume Ratio, period 1 min",fontsize=8)
vol15.tick_params(axis='both', which='major', labelsize=8)
vol15.locator_params(axis='x', nbins=4)
vol15.set_yticks(yrange)


vol30 = f.add_subplot(5,3,11)
vol30.set_title("Volume Ratio, period 5 min",fontsize=8)
vol30.tick_params(axis='both', which='major', labelsize=8)
vol30.locator_params(axis='x', nbins=4)
vol30.set_ylim([0,1])


cor15 = f.add_subplot(5,3,13)
cor15.set_title("Moving Correlation, period 3 min",fontsize=8)
cor15.tick_params(axis='both', which='major', labelsize=8)
cor15.locator_params(axis='x', nbins=6)
cor15.set_ylim([0,1])

cor30 = f.add_subplot(5,3,14)
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

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace= 0.45)
def update(self,PT,readlock):

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
			# xtick = cur_time
			# if len(cur_time)>6:
			# 	xtick = cur_time[::len(cur_time)//5]

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
			d_reg.append(d_intcep+d_slope*newd2[-1])

			w_reg.append(w_intcep+w_slope*newd[-1])

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
			
			cur = round((intra_spread[-1] - intra_spread5[-1])/intra_std[-1],2)


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
				cor15.plot(cur_minute,cor_15)
				cor15.set_yticks(yrange_cor)
				cor15.set_title("Correlation 3 min: Current : "+ str(round(cor_15[-1],2)),fontsize=8)

				cor30.clear()
				cor30.plot(cur_minute,cor_30)
				cor30.set_yticks(yrange_cor)
				cor30.set_title("Correlation 15 min: Current : "+ str(round(cor_30[-1],2)),fontsize=8)

				#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

				vol15.legend(fontsize=6,loc="upper left")
				vol30.legend(fontsize=6,loc="upper left")


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



def start(test,readlock):
	global f
	ani = FuncAnimation(f,update,fargs=(test,readlock),interval=5000)

	plt.show()
plt.show()