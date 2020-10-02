import time
import random
import subprocess
import datetime
import Meta_extractor_lib
import pandas as pd
import numpy as np

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


#STEP 1, Log in
print("Registering...")
postbody = "http://api.kibot.com/?action=login&user=sajali26@hotmail.com&password=guupu4upu"
r= requests.post(postbody)


#STEP 2, DOWNLOAD DATA
if r.status_code==200:

    now = datetime.datetime.now()
    time_str = '_{}_{}'.format('{:02d}'.format(now.month), '{:02d}'.format(now.day))
    time_min = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute), '{:02d}'.format(now.second))

    postbody = "http://api.kibot.com/?action=history&symbol=SPY&interval=1&period=5"

    spy = "SPY"+time_str+".txt"
    qqq = "QQQ"+time_str+".txt"
    success = 0

    r= requests.post(postbody)
    if r.status_code==200:
        t=r.text
        with open("data/"+spy, "w") as text_file:
            text_file.write(t)

        print("SPY data update at:",time_min)
        success+=1
    else:
        print("Failed to get data from SPY")

    postbody = "http://api.kibot.com/?action=history&symbol=QQQ&interval=1&period=5"
    r= requests.post(postbody)
    if r.status_code==200:
        t=r.text
        with open("data/"+qqq, "w") as text_file:
            text_file.write(t)
        print("QQQ data update at:",time_min)
        success+=1
    else:
        print("Failed to get data from QQQ")


    # update = []
    # #Step 2 Meta process
    # if success ==2:
    #     update = Meta_extractor_lib.stat_extractor([spy,qqq])
            

    #     #Step 4 git hub upload
    #     if len(update)>0:
    #         continue
    #error from step2


#error from Step1 
else:
    print("Failed to registrate, abort.")










    #check if the files are there now. 


    ## Run every 30 minutes. 