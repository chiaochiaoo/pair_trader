import time
import random
import subprocess
import datetime
import Meta_extractor_lib
import Spread_extractor_lib
import pandas as pd
import numpy as np
import os
import sys

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




# Mode. Auto Run

# Mode. Fectch current volume. 

# subprocess.call(["python", "test.py"])
# print(t)

#STEP 1, Log in


def auto_run():
    while True:

        now = datetime.datetime.now()
        #time_str = '{}_{}_{}'.format()
        time_min = '{}_{}_{}:{}:{}'.format('{:02d}'.format(now.month), '{:02d}'.format(now.day),'{:02d}'.format(now.hour), '{:02d}'.format(now.minute), '{:02d}'.format(now.second))

        print("Database: System running at: ",time_min)
        print("Database: Registering...")
        postbody = "http://api.kibot.com/?action=login&user=sajali26@hotmail.com&password=guupu4upu"
        r= requests.post(postbody)

        #STEP 2, DOWNLOAD DATA
        if r.status_code==200:

            postbody = "http://api.kibot.com/?action=history&symbol=SPY&interval=1&period=30"

            spy = "SPY"+".txt"
            qqq = "QQQ"+".txt"
            temp = "data/"
            d= "data/"
            success = 0

            r= requests.post(postbody)
            if r.status_code==200:
                t=r.text
                with open(temp+spy, "w") as text_file:
                    text_file.write(t)

                print("Database: SPY data update at:",time_min)
                success+=1
            else:
                print("Database: Failed to get data from SPY")

            postbody = "http://api.kibot.com/?action=history&symbol=QQQ&interval=1&period=30"
            r= requests.post(postbody)
            if r.status_code==200:
                t=r.text
                with open(temp+qqq, "w") as text_file:
                    text_file.write(t)
                print("Database: QQQ data update at:",time_min)
                success+=1
            else:
                print("Database: Failed to get data from QQQ")

            update = []
            #Step 2 Meta process
            if success ==2:
                update = Meta_extractor_lib.stat_extractor([temp+spy,temp+qqq])

                update.append(Spread_extractor_lib.spread_extractor([temp+spy,temp+qqq,"SPY","QQQ"]))
                print(update)
                #Step 4 git hub upload
                
                if len(update)>0:
                    subprocess.call(["git", "pull"])
                    for i in update:
                        subprocess.call(["git", "add",i])

                    subprocess.call(["git", "commit","--m","update at "+time_min])

                    subprocess.call(["git", "push"])
            #error from step2


        #error from Step1 
        else:
            print("Database: Failed to registrate, abort.")


        print("Database: Cycle completed. Sleep for 30 minutes")
        time.sleep(1800)


def fetch_volume(symbols):

    postbody = "http://api.kibot.com/?action=login&user=sajali26@hotmail.com&password=guupu4upu"
    r= requests.post(postbody)

    #STEP 2, DOWNLOAD DATA
    volume = []
    if r.status_code==200:
        symbols = "".join([i+"," for i in symbols])[:-1]
        postbody = "http://api.kibot.com/?action=snapshot&symbol="+symbols+"&user=sajali26@hotmail.com&password=guupu4upu"
        r= requests.post(postbody)
        r = r.text
        with open("data/temp.txt", "w") as text_file:
            text_file.write(r)
        res = pd.read_csv("data/temp.txt")

        res = res["Volume"].tolist()

        if len(res)>0:
            print("Fetching volume from database successful")

        return res


if not os.path.exists("data"):
    os.mkdir("data")

if len(sys.argv)>1:
    if sys.argv[1] == "a":
        auto_run()

# http://api.kibot.com/?action=snapshot&symbol=SPY,QQQ

