import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
import sys


if not os.path.exists("report"):
    os.mkdir("report")

file = sys.argv[1]

S =pd.read_csv('data/'+file+'stat.csv')

if len(S) < 100:


    print("File read unsuccesfful")

else:
    print("File read succesfful")
    ak = S.keys()[3::3]
    sk = S.keys()[4::3]

    start=S[S['time']=='04:00'].index.values[0]

    S=S[start:]
    t = S.keys()[2]
    t =  pd.to_datetime(S[t],format='%H:%M')
    start=S[S['time']=='09:30'].index.values[0]
    end=S[S['time']=='16:00'].index.values[0]+1

    fig, axs = plt.subplots(5, 2,figsize=(15,15))
    fig.canvas.set_window_title('INCLUDING PRE-MARKET')
    min_form = DateFormatter("%H:%M")

    titles = ["Volume 1 min average","Volume 5 min average","Volume 30 min average", "Volume accumulative average"\
            ,"Range 1 min average","Range 5 min average","Range 30 min average"\
            ,"ROC 1 min average","ROC 5 min average","ROC 30 min average"]
    k=0
    for i in range(5):
        for j in range(2):
            if i >=1 and j==3:
                axs[i,j].axis('off')
            else:
                mean = np.array(S[ak[k]],dtype=float)
                std = np.array(S[sk[k]],dtype=float)
                #print(mean)
                axs[i,j].xaxis.set_major_formatter(min_form)
                axs[i,j].xaxis.set_major_locator(mdates.MinuteLocator(interval=90)) 
                axs[i,j].plot(t,mean)
                
                axs[i,j].fill_between(t.values,mean+std,mean-std,alpha=0.23)
                
                axs[i,j].set_title(titles[k])
                axs[i,j].axvline(t[start],c="r",linestyle="--",linewidth=1 ,label='open')
                axs[i,j].axvline(t[end],c="r",linestyle="--",linewidth=1 ,label='close')
                axs[i,j].legend()
                k+=1
    #fig.autofmt_xdate() 

    plt.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace= 0.45)

    plt.savefig(file+'_stats_premarket.png')

    S=S[start:end]
    t = S.keys()[2]
    t =  pd.to_datetime(S[t],format='%H:%M')
    fig2, axs = plt.subplots(5, 2,figsize=(15,15))
    fig2.canvas.set_window_title('MARKET HOURS ONLY')
    #min_form = DateFormatter("%H:%M")

    titles = ["Volume 1 min average","Volume 5 min average","Volume 30 min average", "Volume accumulative average"\
            ,"Range 1 min average","Range 5 min average","Range 30 min average"\
            ,"ROC 1 min average","ROC 5 min average","ROC 30 min average"]
    k=0
    for i in range(5):
        for j in range(2):
            if i >=1 and j==3:
                axs[i,j].axis('off')
            else:
                mean = np.array(S[ak[k]],dtype=float)
                std = np.array(S[sk[k]],dtype=float)
                #print(mean)
                axs[i,j].xaxis.set_major_formatter(min_form)
                axs[i,j].xaxis.set_major_locator(mdates.MinuteLocator(interval=30)) 
                axs[i,j].plot(t,mean)
                
                axs[i,j].fill_between(t.values,mean+std,mean-std,alpha=0.23)
                
                axs[i,j].set_title(titles[k])
    #             axs[i,j].axvline(t[start],c="r",linestyle="--",linewidth=1 ,label='open')
    #             axs[i,j].axvline(t[end],c="r",linestyle="--",linewidth=1 ,label='close')
                k+=1
    #fig2.autofmt_xdate() 

    plt.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace= 0.45)
    plt.savefig(file+'_stats_market.png')
    plt.show()