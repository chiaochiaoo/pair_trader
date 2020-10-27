import sys

try:
    import requests
except ImportError:
    import pip 
    pip.main(['install', 'requests'])
    import requests

try:
    import json
except ImportError:
    import pip 
    pip.main(['install', 'json'])
    import json

try:
    import pandas as pd
except ImportError:
    import pip 
    pip.main(['install', 'pandas'])
    import pandas as pd

from datetime import datetime


def get_first_option(symbol):
    querystring = {"symbol":symbol,"region":"US"}
    url = "https://rapidapi.p.rapidapi.com/stock/v2/get-options"

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "0da8e9b784msh9001cc4bfc4e7e7p1c6d94jsna54c1aa52dbf"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    res = response.text
    res = json.loads(res)
    
    all_dates = get_dates(res)
    
    return res,all_dates

def get_option(symbol,timestamp):
    querystring = {"symbol":symbol,"date":timestamp,"region":"US"}
    url = "https://rapidapi.p.rapidapi.com/stock/v2/get-options"

    headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': "0da8e9b784msh9001cc4bfc4e7e7p1c6d94jsna54c1aa52dbf"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    res = response.text
    res = json.loads(res)
    
    return res

def get_dates(res):
    return res['meta']['expirationDates']

def missing_values(res):
    for i in range(len(res['contracts']['calls'])):
        if "volume" not in res['contracts']['calls'][i]:
            res['contracts']['calls'][i]["volume"]={}
            res['contracts']['calls'][i]["volume"]["fmt"] = None
        if "openInterest" not in res['contracts']['calls'][i]:
            res['contracts']['calls'][i]["openInterest"]={}
            res['contracts']['calls'][i]["openInterest"]["fmt"] = None
        if "openInterest" not in res['contracts']['calls'][i]:
            res['contracts']['calls'][i]["openInterest"]={}
            res['contracts']['calls'][i]["openInterest"]["fmt"] = None
        if "openInterest" not in res['contracts']['calls'][i]:
            res['contracts']['calls'][i]["openInterest"]={}
            res['contracts']['calls'][i]["openInterest"]["fmt"] = None
        if "openInterest" not in res['contracts']['calls'][i]:
            res['contracts']['calls'][i]["openInterest"]={}
            res['contracts']['calls'][i]["openInterest"]["fmt"] = None
            
            
    for i in range(len(res['contracts']['puts'])):
        if "volume" not in res['contracts']['puts'][i]:
            res['contracts']['puts'][i]["volume"] = {}
            res['contracts']['puts'][i]["volume"]["fmt"] = None 
        if "openInterest" not in res['contracts']['puts'][i]:
            res['contracts']['puts'][i]["openInterest"]={}
            res['contracts']['puts'][i]["openInterest"]["fmt"] = None


def try_garb(res,type_):

    if type_ in res:
        # if a dictionary 
        if type(res[type_])==type({}):
            if "fmt" in res[type_]:
                return res[type_]['fmt']
            #or just return the first key 
            else:
                return res[type_][list(res[type_].keys())[0]]
        else:
            return res[type_]
    else:
        return None

def add_options_to_list(res,ls):
    missing_values(res)
    for i in range(len(res['contracts']['calls'])):
        ls.append([res['contracts']['calls'][i]["contractSymbol"],\
                      "calls",
        try_garb(res['contracts']['calls'][i],"currency"),\
        try_garb(res['contracts']['calls'][i],"inTheMoney"),\
        try_garb(res['contracts']['calls'][i],"impliedVolatility"),\
        try_garb(res['contracts']['calls'][i],"expiration"),\
        try_garb(res['contracts']['calls'][i],"change"),\
        try_garb(res['contracts']['calls'][i],"strike"),\
        try_garb(res['contracts']['calls'][i],"contractSize"),\
        try_garb(res['contracts']['calls'][i],"lastPrice"),\
        try_garb(res['contracts']['calls'][i],"openInterest"),\
        try_garb(res['contracts']['calls'][i],"percentChange"),\
        try_garb(res['contracts']['calls'][i],"ask"),\
        try_garb(res['contracts']['calls'][i],"bid"),\
        try_garb(res['contracts']['calls'][i],"volume"),\
        try_garb(res['contracts']['calls'][i],"lastTradeDate")])

    for i in range(len(res['contracts']['puts'])):
        ls.append([res['contracts']['puts'][i]["contractSymbol"],\
                     "puts",
        try_garb(res['contracts']['puts'][i],"currency"),\
        try_garb(res['contracts']['puts'][i],"inTheMoney"),\
        try_garb(res['contracts']['puts'][i],"impliedVolatility"),\
        try_garb(res['contracts']['puts'][i],"expiration"),\
        try_garb(res['contracts']['puts'][i],"change"),\
        try_garb(res['contracts']['puts'][i],"strike"),\
        try_garb(res['contracts']['puts'][i],"contractSize"),\
        try_garb(res['contracts']['puts'][i],"lastPrice"),\
        try_garb(res['contracts']['puts'][i],"openInterest"),\
        try_garb(res['contracts']['puts'][i],"percentChange"),\
        try_garb(res['contracts']['puts'][i],"ask"),\
        try_garb(res['contracts']['puts'][i],"bid"),\
        try_garb(res['contracts']['puts'][i],"volume"),\
        try_garb(res['contracts']['puts'][i],"lastTradeDate")])



def get_all_options(symbol):
    
    cols=['contractSymbol','type','currency', 'inTheMoney',  \
          'impliedVolatility', 'expiration', 'change',  \
          'strike', 'contractSize', 'lastPrice',\
          'openInterest', 'percentChange', 'ask', 'bid','volume', 'lastTradeDate', ]

    res, dates = get_first_option(symbol)
    
    ls = []
    print("Processing date:","{: %Y-%m-%d}".format(datetime.fromtimestamp(dates[0]+1)))
    add_options_to_list(res,ls)
    
    
    #now add the remaining ones. 
    for i in range(1,len(dates)):
        print("Processing date:","{: %Y-%m-%d}".format(datetime.fromtimestamp(dates[i]+1)))
        res = get_option(symbol,dates[i])
        add_options_to_list(res,ls)
    
    
    df = pd.DataFrame(ls,columns=cols)
    df.to_csv(symbol+"_options.csv",index=False)
    


symbol = sys.argv[1]

get_all_options(symbol)