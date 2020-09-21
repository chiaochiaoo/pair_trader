# import os.path
# from os import path
# import sys

from datetime import date
import time
import random

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

LastPrice ={}
LastTime = {}
#############################################
######## ONE TRHEAD - ONE SYMBOL ? ############
#############################################


#### THIS IS THE ONLY FUNCTION THAT NEEDS TO BE CALLED.
def TOS_init(Symbols,Price,Volume,Lock,Realmode):

    Hello()
    if Realmode == False:
        print("Console (TOS): Initializing simulation mode")
        Testmode(Symbols,Price,Volume,Lock)
    else:    
        if Register(Symbols,4050,Price,Volume):
            print("Console (TOS): Data receiving begins")
            Portwatcher(Symbols,4050,Price,Volume,Lock)


def Testmode(Symbols,Price,Volume,Lock):

    while True:
        with Lock:
            for i in Symbols:
                # Price[i].append(c)
                # Volume[i].append(c)
                Price[i].append(random.randint(1,50))
                Volume[i].append(random.randint(100,200))
        time.sleep(0.000000001)

def Hello():
    print("Console (TOS): TOS Moudule initializing...")

def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return data

# symbol = ['SPY.AM','QQQ.NQ"]
def Register(SYMBOLLIST,PORT,Price,Volume):

        global LastPrice
        global LastTime
    
        print("Registering...")
        for i in SYMBOLLIST:
            postbody = "http://localhost:8080/SetOutput?symbol=" + i + "&region=1&feedtype=TOS&output=" + str(PORT)+"&status=on"
            r= requests.post(postbody)
            if (r.status_code!=200):
                print("registration failed. Trying new port:" ,PORT)
                return False

        print("All symbols resigstered:",SYMBOLLIST)

        for i in SYMBOLLIST:

        	Price[i] = []
        	Volume[i] = []
        	LastTime[i] = 0
        	LastPrice[i] = 0

        return True


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def Portwatcher(SYMBOLLIST,PORT,Price,Volume,Lock):

    global LastPrice
    global LastTime
    global Registration

    UDP_IP = "127.0.0.1"
    UDP_PORT = PORT

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print("Console (TOS) : Socket Created:",sock)
    
    # Registration = True 

    # for i in SYMBOLLIST:
    
    #     file_name =   "data" + "/"+ i + "_TOS_" +str(date.today())[5:]+".csv"

    #     if not path.exists(file_name):
    #         with open(file_name, 'w',newline='') as csvfile:
    #             writer = csv.writer(csvfile)
    #             writer.writerow(['timestamp','time', 'price','size'])
                
    # for i in SYMBOLLIST:
    
    #     file_name =  "data" + "/"+i + "_Processed_" + str(date.today())[5:] + ".csv"

    #     if not path.exists(file_name):
    #         with open(file_name, 'w',newline='') as csvfile:
    #             writer = csv.writer(csvfile)
    #             writer.writerow(['timestamp', 'time','price','MA5','MA10','MA20','MA30','MA60','size'])
    
    ###################################################################

    while True:
        data, addr = sock.recvfrom(1024)
        stream_data = str(data)
        
        ##### Slice directly. 
        symbol = find_between(stream_data, "Symbol=", ",")
        time = find_between(stream_data, "MarketTime=", ",")
        timestamp = get_sec(time[:-4])
        size = int(find_between(stream_data, "Size=", ","))
        price = float(find_between(stream_data, "Price=", ","))
    
        #append this data to the milisecond CSV.
        # file_name =   "data" + "/"+i + "_TOS_" +str(date.today())[5:]+".csv"
        # with open(file_name, 'a',newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow([timestamp,time[:-4],price,size])
            
        #process this data to the Data Processor. 


        if LastPrice[symbol] ==0:
            with Lock:
                Price[symbol].append(price)
                Volume[symbol].append(size)    

        elif timestamp >= LastTime[symbol]-2 and abs(price-LastPrice[symbol])/LastPrice[symbol]<0.01:

        	#data_processor(symbol,timestamp//1000,size,price)

        	#Put it into a Temp Table. 
            with Lock:
            	Price[symbol].append(price)
            	Volume[symbol].append(size)


        LastTime[symbol] = timestamp
        LastPrice[symbol] = price

        #print(countx)



'LocalTime=11:52:51.495,Message=TOS,MarketTime=11:52:51.911,Symbol=TSLA.NQ,Type=0,Price=443.4900,Size=10,Source=1,Condition=X,Tick=?,Mmid=T,SubMarketId=32,Date=2020-09-15,BuyerId=0,SellerId=0\n'
