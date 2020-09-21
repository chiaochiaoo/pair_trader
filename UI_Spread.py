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

	
plt.style.use("seaborn-darkgrid")
f = plt.figure(1,figsize=(10,15))
f.canvas.set_window_title('SPREAD MONITOR')


def report(spy,qqq,sma,std):

	n = round(((spy-qqq)-sma)/std,2)

	text = ""
	if n >=0:
		text = "+" + str(n) + "STD away from the mean"
	else:
		text = "-" + str(n) + "STD away from the mean"
		print("g")

	return text


SPY = np.array([311.56, 310.19, 310.37, 308.56, 310.68, 312.03, 304.12, 307.31, 300.01, 304.43, 308.57, 310.57, 312.18, 316.99, 313.72, 316.12, 314.42, 317.61, 314.81, 318.89, 321.865, 320.81, 321.67, 324.36, 324.96, 326.82, 322.935, 320.86, 323.18, 321.2, 325.09, 323.98, 326.55, 328.76, 330.02, 332.06, 334.31, 334.55, 335.55, 332.82, 337.42, 336.86, 336.86, 337.88, 338.62, 337.22, 338.25, 339.44, 342.94, 344.0999, \
347.56, 348.29, 350.54, 349.35, 352.56, 357.68, 345.41, 342.6, 333.26, 339.76,339.89,334.06,338.46, 342.14	,342.14])
QQQ = np.array([242.53, 243.14, 243.87, 243.74, 246.77, 248.73, 243.78, 246.08, 240.08, 242.77, 247.28, 250.43, 252.11, 258.39, 256.56, 259.94, 262.06, 264.01, 258.53, 260.41, 260.78, 258.98, 259.38, 266.79, 264.05, 264.92, 257.95, 255.44, 260.09, 256.76, 259.83, 261.16, 265.84, 269.31, 270.44, 271.11, 274.585, 271.5, 270.28, 265.21, 271.93, 272.48, 272.22, 275.27, 277.962, 276.14, 279.88, 281.85, 283.61, 285.82, \
291.88, 290.99, 292.5, 294.99, 299.89, 302.73, 287.21, 283.47, 270.01, 277.78,272.34	,270.45,275.16	, 278.88	,278.88])
GAP = SPY-QQQ
STD = chiao.MovingStd(GAP,10)
SMA = chiao.SMA(GAP,10)

dates = np.array(['06/16/2020', '06/17/2020', '06/18/2020', '06/19/2020', '06/22/2020', '06/23/2020', '06/24/2020', '06/25/2020', '06/26/2020', '06/29/2020', '06/30/2020', '07/01/2020', '07/02/2020', '07/06/2020', '07/07/2020', '07/08/2020', '07/09/2020', '07/10/2020', '07/13/2020', '07/14/2020', '07/15/2020', '07/16/2020', '07/17/2020', '07/20/2020', '07/21/2020', '07/22/2020', '07/23/2020', '07/24/2020', '07/27/2020', '07/28/2020', '07/29/2020', '07/30/2020', '07/31/2020', '08/03/2020', '08/04/2020', '08/05/2020', '08/06/2020', '08/07/2020', '08/10/2020', '08/11/2020', '08/12/2020', '08/13/2020', '08/14/2020', '08/17/2020', '08/18/2020', '08/19/2020', '08/20/2020', '08/21/2020', '08/24/2020', '08/25/2020', '08/26/2020', '08/27/2020', '08/28/2020', '08/31/2020', '09/01/2020', '09/02/2020', '09/03/2020', \
'09/04/2020', '09/08/2020', '09/09/2020','09/10/2020','09/11/2020','09/14/2020','09/15/2020','09/16/2020'])
dates = pd.to_datetime(dates)


hist_spread = f.add_subplot(521)#add_axes([0.1, 0.1, 0.78, 0.78])
# hist_spread.plot(dates,GAP,"r",label="Spread")
# hist_spread.plot(dates,SMA,"c",label="Spread SMA10")
# hist_spread.fill_between(dates, SMA-2*STD,SMA+2*STD,alpha=0.23,label="Price gap deviation zone")



daily_spread = f.add_subplot(512)
daily_spread.set_title("Intraday Spread",fontsize=8)
daily_spread.tick_params(axis='both', which='major', labelsize=8)


roc = f.add_subplot(513)
roc.set_title("Rate of Change Difference: SPY - QQQ",fontsize=8)
roc.tick_params(axis='both', which='major', labelsize=8)
roc.locator_params(tight=True, nbins=6)

vol = f.add_subplot(527)
vol.set_title("Volume Ratio, period 15 min",fontsize=8)
vol.tick_params(axis='both', which='major', labelsize=8)
vol.locator_params(tight=True, nbins=6)

vol = f.add_subplot(528)
vol.set_title("Volume Ratio, period 15 min",fontsize=8)
vol.tick_params(axis='both', which='major', labelsize=8)
vol.locator_params(tight=True, nbins=6)

cor = f.add_subplot(529)
cor.set_title("Moving Correlation, period 15 min",fontsize=8)
cor.tick_params(axis='both', which='major', labelsize=8)

cor = f.add_subplot(5,2,10)
cor.set_title("Moving Correlation, period 30 min",fontsize=8)
cor.tick_params(axis='both', which='major', labelsize=8)

# cor2 = f.add_subplot(5,2,10)
# cor2.set_title("Moving Correlation, period 15 min",fontsize=8)
# cor2.tick_params(axis='both', which='major', labelsize=8)

min_form = DateFormatter("%H:%M:%S")
daily_spread.xaxis.set_major_formatter(min_form)
vol.xaxis.set_major_formatter(min_form)


text = "alert window:                                                                            \n"
info = \
"                                                                          \n\
                                                                           \n\
                                                                           \n\
                                                                           \n"

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.5, 0.81, text+info, fontsize=11, transform=plt.gcf().transFigure,bbox=props, verticalalignment='center')

plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace= 0.45)
plt.show()