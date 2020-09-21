import numpy as np
from scipy.stats import pearsonr 


def mean(lst):
    if len(lst)>0:
        return sum(lst)/len(lst)
    else:
        print("mean function error, length must not be zero.")
        return None

def MovingStd(lst,period):
    k = []
    k.append(0)
    for i in range(1,len(lst)):
        if i < period:
            k.append(np.std(lst[:i]))
        else:
            k.append(np.std(lst[i-period+1:i+1]))
            
    return np.array(k)

def vwap(lst1,lst2):

    if len(lst1) != len(lst2):
        print("Vwap failed. length not matched.")
        return None 

    sum_ = 0
    price = 0 
    for i in range(len(lst1)):
        price += lst1[i]*lst2[i] 
        sum_ += lst2[i]
    return round(price/sum_,2)

def vwap_multiperiods(vwaps,vols):

    if len(lst1) != len(lst2):
        print("Vwap failed. length not matched.")
        return None 

    return vwap(vwaps,vols)


def roc(lst1):
    lst =[]
    lst.append(0)
    lst.extend(np.diff(lst1))
    
    return np.array(lst)


def SMA(lst,n):
    lst1= []
    lst1.append(lst[0])
    for i in range(1,len(lst)):
        if i < n:
            lst1.append(mean(lst[:i+1]))
        else:
            lst1.append(mean(lst[i-n+1:i+1]))
            
    return np.array(lst1)

def EMA(lst,n):
    weight= []
    for i in range(n):
        weight.append(2**i)

    Sum = sum(weight)
    normalize = np.array(weight)/Sum

    EMA =[]

    lst = SMA(lst,n)

    EMA.append(lst[0])
    for i in range(1,len(lst)):
        if i<n-1:
            EMA.append(sum(lst[:i+1]*normalize[:i+1])/sum(normalize[:i+1]))
        else:
            EMA.append(sum(lst[i-n+1:i+1]*normalize))

    return EMA

def cor(lst1,lst2):

    if len(lst1)!=len(lst2):
        print("Correlation calculation failed, length not matched")
        return None 
    else:
        return(pearsonr(lst1,lst2)[0])

def cor_period(lst1,lst2,period):

    if len(lst1)!=len(lst2):
        print("Correlation calculation failed, length not matched")
        return None 
    else:
        return(pearsonr(lst1[:-period],lst2[:-period])[0])


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


#### String, milisecond => timestamp 
def get_milisec(time_str,mili):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return 1000*(int(h) * 3600 + int(m) * 60 + int(s))+int(mili)


# import datetime
# now = datetime.datetime.now()

# time = '{}:{}:{}'.format('{:02d}'.format(now.hour), '{:02d}'.format(now.minute),  '{:02d}'.format(now.second))

# print(time)