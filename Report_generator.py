import time
import random
import subprocess
import datetime
import Meta_extractor_lib
import pandas as pd
import numpy as np
import os
import sys
import os

try:
    import requests
except ImportError:
    import pip 
    pip.main(['install', 'requests'])
    import requests

try:
    import socket
except ImportError:
    import pip 
    pip.main(['install', 'socket'])
    import socket


# subprocess.call(["python", "test.py"])
# print(t)

def ts_to_str(timestamp):
    
    h= int(timestamp//60)
    m= int(timestamp%60)

    #chekc if they are 1 unit.
    
    if h//10 == 0:
        h = "0"+str(h)
    else:
        h = str(h)
        
    if m//10 == 0:
        m = "0"+str(m)
    else:
        m = str(m)
        
    return(h+":"+m)

def printer(d,name):
    #d is a seires of timestamp
    skip=0
    s=""
    for i in d:
        j = 0
        if i >skip:
            while (i+j in d) or (i+j+1 in d) or (i+j+2 in d):
                j+=1  

            if j ==0:
                #print(name,ts_to_str(i))
                s+=(name+ts_to_str(i)+"\n")
            else:
                #print(name,ts_to_str(i),"-",ts_to_str(i+j))
                s+= (name+ts_to_str(i)+"-"+ts_to_str(i+j)+" \n")
                skip=i+j
                #print(ts_to_str(skip))
    return s
    


def report(symbol):
    S =pd.read_csv('data/'+symbol+'stat.csv')

    start=S[S['time']=='09:30'].index.values[0]
    end=S[S['time']=='16:00'].index.values[0]+1

    vol1_avg = np.mean(S["v1m"][start:end])
    vol5_avg = np.mean(S["v5m"][start:end])
    vol30_avg = np.mean(S["v30m"][start:end])

    vol1_std = np.std(S["v1m"][start:end])
    vol5_std = np.std(S["v5m"][start:end])
    vol30_std = np.std(S["v30m"][start:end])

    range_avg= np.mean(S["rm"][start:end])
    range_std= np.std(S["rm"][start:end])

    range5_avg= np.mean(S["r5m"][start:end])
    range5_std= np.std(S["r5m"][start:end])

    range30_avg = np.mean(S["r30m"][start:end])
    range30_std= np.std(S["r30m"][start:end])

    roc_avg= np.mean(S["rocm"][start:end])
    roc_std= np.std(S["rocm"][start:end])

    roc5_avg= np.mean(S["roc5m"][start:end])
    roc5_std= np.std(S["roc5m"][start:end])

    roc30_avg= np.mean(S["roc30m"][start:end])
    roc30_std= np.std(S["roc30m"][start:end])


    v1=[]
    v5=[]
    v30=[]
    d= []
    d5=[]
    d30=[]
    roc=[]
    roc5=[]
    roc30=[]
    for i in range(len(S)):
        if S["rm"][i]>range_avg+range_std*2:
            d.append(S["timestamp"][i]-1)
        if S["r5m"][i]>range5_avg+range5_std*2:
            d5.append(S["timestamp"][i]-5)
        if S["r30m"][i]>range30_avg+range30_std*2:
            d30.append(S["timestamp"][i]-30)        
            
        if S["v1m"][i]>vol1_avg+vol1_std*2:
            v1.append(S["timestamp"][i]-1)
        if S["v5m"][i]>vol5_avg+vol5_std*2:
            v5.append(S["timestamp"][i]-5)
        if S["v30m"][i]>vol30_avg+vol30_std*2:
            v5.append(S["timestamp"][i]-30)
            
        if S["rocm"][i]>roc_avg+roc_std*2:
            roc.append(S["timestamp"][i]-1)
        if S["roc5m"][i]>roc5_avg+roc5_std*2:
            roc5.append(S["timestamp"][i]-5)
        if S["roc30m"][i]>roc30_avg+roc30_std*2:
            roc30.append(S["timestamp"][i]-30)
                  
            
            

    ret =''
    ret += printer(d,"1 minute extreme range on average occur during ")
    ret += " \n"

    ret +=printer(d5,"5 minute extreme range on average occur during")   
    ret += " \n"
    ret +=printer(d30,"30 minute extreme range on average occur during")   
    ret += " \n"


    ret +=printer(v1,"1 minute extreme volume on average occur during")
    ret += " \n"
    ret +=printer(v5,"5 minute extreme volume on average occur during")
    ret += " \n"
    ret +=printer(v30,"30 minute extreme volume on average occur during")
    ret += " \n"
    ret +=printer(roc,"1 minute extreme rate of change on average occur during")
    ret += " \n"
    ret +=printer(roc5,"5 minute extreme rate of change on average occur during")
    ret += " \n"
    ret +=printer(roc30,"30 minute extreme volume on average occur during")

    text_file = open("Report_"+symbol+".txt", "w")
    text_file.write("REPORT ON {0}\n{1}".format(symbol,ret))
    text_file.close()
#STEP 1, Log in
if not os.path.exists("report"):
    os.mkdir("report")



for i in range(1,len(sys.argv)):


	symbol = sys.argv[i]
	print("Report Generator: downlowding recent data for...",symbol)


	postbody = "http://api.kibot.com/?action=login&user=sajali26@hotmail.com&password=guupu4upu"
	r= requests.post(postbody)

	#STEP 2, DOWNLOAD DATA
	if r.status_code==200:

	    postbody = "http://api.kibot.com/?action=history&symbol="+symbol+"&interval=1&period=30"

	    file = symbol+".txt"
	    temp = "data/"
	    d= "data/"


	    r= requests.post(postbody)
	    if r.status_code==200:
	        t=r.text
	        with open(temp+file, "w") as text_file:
	            text_file.write(t)

	        print("Report Generator:",symbol," data donwloaded")

	       	Meta_extractor_lib.stat_extractor([temp+file])

	        print("Report Generator:",symbol," stats files created")

	        report(symbol)

	        print("Report Generator:",symbol," report generated")
	    else:
	        print("Database: Failed to get data from",symbol)
	#error from Step1 
	else:
	    print("	Report Generator: Failed to register, abort.")













