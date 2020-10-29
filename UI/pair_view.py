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




plt.style.use("seaborn-darkgrid")
f = plt.figure(1,figsize=(10,15))
f.canvas.set_window_title('SPREAD MONITOR')
min_form = DateFormatter("%H:%M")
gs = f.add_gridspec(4, 3)

a=[1,2,1]
b=[1,2,3]

#set the self plot

spread = f.add_subplot(gs[0,:])
spread.tick_params(axis='both', which='major', labelsize=8)
spread.set_title('IntraDay Spread')
spread.xaxis.set_major_formatter(min_form)

max_spread_m = f.add_subplot(gs[1,0])
max_spread_m.set_title('Max Spread Today')

max_spread_m = f.add_subplot(gs[1,1])
max_spread_m.set_title('Max Spread Weekly')

max_spread_m = f.add_subplot(gs[1,2])
max_spread_m.set_title('Max Spread Monthly')

roc1 = f.add_subplot(gs[2,0])
roc1.set_title('Max Speed 1 min')

roc5 = f.add_subplot(gs[2,1])
roc5.set_title('Max Speed 5 min')

roc15 =f.add_subplot(gs[2,2])
roc15.set_title('Max Speed 15 min')

#plt.tight_layout()
plt.show()