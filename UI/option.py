import sys
import threading
import requests
import json
import pip
from datetime import datetime
from datetime import date

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

try:
    import pandas as pd
except ImportError:
    pip.main(['install', 'pandas'])
    import pandas as pd

try:
    import numpy as np
except ImportError:
    pip.main(['install', 'numpy'])
    import numpy as np

try:
    import matplotlib.pyplot as plt
except ImportError:
    pip.main(['install', 'matplotlib'])
    import matplotlib.pyplot as plt


######################

###### Need to destroy the buttons and labels when a new symbols are loaded. 

##.destroy()



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

            if type_ == "expiration":
                return res[type_]['fmt']
            if "raw" in res[type_]: 
                return res[type_]['raw']
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

def get_all_options(symbol,ui):

    cols=['contractSymbol','type','currency', 'inTheMoney',  \
          'impliedVolatility', 'expiration', 'change',  \
          'strike', 'contractSize', 'lastPrice',\
          'openInterest', 'percentChange', 'ask', 'bid','volume', 'lastTradeDate', ]

    res, dates = get_first_option(symbol)

    ls = []

    percentage = int((1/len(dates))*100)

    ui.status['text'] ="Downloading data and Forecasting... 0 %"
    add_options_to_list(res,ls)

    #now add the remaining ones.
    #for i in range(1,2):

    for i in range(1,min(len(dates),5)):
        #ui.status['text'] ="Processing date:","{: %Y-%m-%d}".format(datetime.fromtimestamp(dates[i]+3600*5))
        ui.status['text'] ="Downloading data and Forecasting... "+str(percentage*i)+" %"
        res = get_option(symbol,dates[i])
        add_options_to_list(res,ls)

    df = pd.DataFrame(ls,columns=cols)
    #df.to_csv(symbol+"_options.csv",index=False)
    return df

def days_counter(dates):

    today = date.today().strftime("%Y-%m-%d")

    length = []

    diff = 0
    now = datetime.now()
    hour = int(now.strftime("%H"))
    if hour>=16:
        diff = -1

    for i in dates:
        length.append(len(pd.bdate_range(start=today, end=i).day)+diff)

    return length


def most_oi(df,dates):
    ls = []
    for i in dates:
        d = i
        p = df.loc[(df["expiration"]==d)&(df["type"]=="puts")].copy().reset_index()
        p = p.loc[p["openInterest"]==max(p["openInterest"])].copy().reset_index()
        strike=p["strike"].values[0]
        bid = p["bid"].values[0]
        ls.append((strike,bid))
    return ls

def oi_str(oi):
    s = []

    for i in oi:
        s.append("Strike: "+str(i[0])+", Ask: "+str(i[1]))

    return s

def report(dates,dates_count,price_1,price_2,df):

    list1 = []
    list2 = []

    for i in range(len(dates)):

        target1 = df.loc[(df["expiration"]==dates[i])&(df["type"]=="puts")&(df["strike"]<price_1[dates_count[i]][0])].copy().reset_index()
        target2 = df.loc[(df["expiration"]==dates[i])&(df["type"]=="puts")&(df["strike"]<price_2[dates_count[i]][0])].copy().reset_index()

        #Second, pick the highest bid

        strike1 = 0
        bid1 =0
        strike2 =0
        bid2 = 0

        if len(target1)>0:
            target1 = target1.loc[target1["bid"]==max(target1["bid"])].copy().reset_index()
            target1 = target1.loc[target1["strike"]==min(target1["strike"])]
            strike1 = target1["strike"].values[0]
            bid1 = target1["bid"].values[0]
        if len(target2)>0:
            target2 = target2.loc[target2["bid"]==max(target2["bid"])].copy().reset_index()
            target2 = target2.loc[target2["strike"]==min(target2["strike"])]
            strike2 = target2["strike"].values[0]
            bid2 = target2["bid"].values[0]
        #Third, pick the lowest strike. 


        list1.append((round(strike1,2),round(bid1,2)))
        list2.append((round(strike2,2),round(bid2,2)))

    return list1,list2


def HV(p):
    
    #np.diff over price itself.
    x = np.array(p)
    x = x[1:]/x[:-1]
    x = np.log(x)
    x = x - np.mean(x)
    x = np.power(x,2)
    x = np.sqrt(sum(x)* 252* (1/(len(x)-1)))

    return x

#S*V*M*SQRT(n/252)

#estimate range of day N.
def STD(S,V,d):

    dev = []

    for i in range(1,d+1):
        dev.append(S*V*np.sqrt(i/252))

    return np.array(dev)

def implied_vol(hv,d):

    deviations = []

    for i in range(1,d+1):
        deviations.append(S*V*np.sqrt(i/252))

    return np.array(deviations)


def download_daily(i,days):

    postbody = "http://api.kibot.com/?action=login&user=sajali26@hotmail.com&password=guupu4upu"
    r= requests.post(postbody)

    postbody = "http://api.kibot.com/?action=history&symbol="+str(i)+"&interval=daily&period="+str(days)+"&regularsession=1"
    r= requests.post(postbody)
    if r.status_code==200:
        print("Donwload "+i+" successful. Writing to files")
        r = r.text
        with open("temp", "w") as text_file:
            text_file.write(r)

        print("Writing "+i+" completed.")
        j = pd.read_csv("temp",names=["day","open","high","low","close","volume"])

    return j

def price_range(cur_price,dev):

    price_1 = []
    price_2 = []
    for i in range(len(dev)):
        #print(dev[i])
        if cur_price-dev[i]>0:
            price_1.append((round(cur_price-dev[i],2),round(cur_price+dev[i],2)))
        else:
            price_1.append((0,cur_price+dev[i]))
        if cur_price-dev[i]*2>0:
            price_2.append((round(cur_price-dev[i]*2,2),round(cur_price+dev[i]*2,2)))
        else:
            price_2.append((0,round(cur_price+dev[i]*2),2))

    return price_1,price_2


def validity_check(symbol):
    symbols=symbol
    postbody = "http://api.kibot.com/?action=snapshot&symbol="+symbols+"&user=sajali26@hotmail.com&password=guupu4upu"
    r= requests.post(postbody)

    if r.text[:3]!="400":
        return True
    else:
        return False

def get_current_info(symbol):

    symbols=symbol
    postbody = "http://api.kibot.com/?action=snapshot&symbol="+symbols+"&user=sajali26@hotmail.com&password=guupu4upu"
    r= requests.post(postbody)
    r = r.text
    with open("temp", "w") as text_file:
        text_file.write(r)
    res = pd.read_csv("temp")

    return res

def database(symbol,days):

    j = download_daily(symbol, days)
    # t = pd.to_datetime(j["day"])
    p = j["close"]
    info = get_current_info(symbol)
    cur_price = info["LastPrice"].values[0]
    dev = STD(cur_price,HV(p[-200:]),days)
    price_1,price_2 = price_range(cur_price,dev)

    return info,price_1,price_2,round(HV(p[-252:])*100,3)


# v = 1

# choices = [
#     ("Automatic",1),
#     ("Regressive",2),
#     ("Stationary",3),
#     ("Bullish⠀⠀",4),
#     ("Bearish⠀⠀",5)
# ]


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    #option_support.set_Tk_var()
    top = Toplevel1 (root)
    #option_support.init(root, top)

    root.mainloop()

def ShowChoice():
    global v
    print(v.get())

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    option_support.set_Tk_var()
    top = Toplevel1 (w)
    option_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None



class Toplevel1:
    def __init__(self, top=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("1019x1031+836+229")
        top.minsize(120, 1)
        top.maxsize(2564, 1421)
        top.resizable(1,  1)
        top.title("Options Forecasting Tool")
        top.configure(background="#d9d9d9")

        self.display = []
        self.threads = []

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.079, rely=0.039, relheight=0.081
                , relwidth=0.854)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Symbol''')
        self.Labelframe1.configure(background="#d9d9d9")

        self.Entry1 = tk.Entry(self.Labelframe1)
        self.Entry1.place(relx=0.138, rely=0.476, height=17, relwidth=0.177
                , bordermode='ignore')
        self.Entry1.configure(background="white")
        self.Entry1.configure(cursor="fleur")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.011, rely=0.476, height=21, width=104
                , bordermode='ignore')
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(text='''Input Symbol''')

        #lambda: change_label_number(2)
        self.Data = tk.Button(self.Labelframe1,command=self.loadsymbol)
        #self.Data = tk.Button(self.Labelframe1,command=lambda: self.test(2))
        self.Data.place(relx=0.379, rely=0.357, height=34, width=127
                , bordermode='ignore')
        self.Data.configure(activebackground="#ececec")
        self.Data.configure(activeforeground="#000000")
        self.Data.configure(background="#d9d9d9")
        self.Data.configure(disabledforeground="#a3a3a3")
        self.Data.configure(foreground="#000000")
        self.Data.configure(highlightbackground="#d9d9d9")
        self.Data.configure(highlightcolor="black")
        self.Data.configure(pady="0")
        self.Data.configure(text='''Load Symbol''')

        self.status = tk.Label(self.Labelframe1)
        self.status.place(relx=0.586, rely=0.476, height=21, width=403
                , bordermode='ignore')
        self.status.configure(background="#d9d9d9")
        self.status.configure(disabledforeground="#a3a3a3")
        self.status.configure(foreground="#000000")
        self.status.configure(text='''Status: waiting for symbol''')


        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.079, rely=0.14, relheight=0.1
                , relwidth=0.85)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Symbol Info''')
        self.Labelframe2.configure(background="#d9d9d9")


        text = ["Symbol:","Last Price:","Target Price:","P/E:","Earning date:","Perf Week","Perf Month","Perf Quarter","Perf Half Y","Perf Year","Weekly Volitality:","Monthly Volitality:",]
        self.info = []
        for i in range(len(text)*2): #Rows
            if i%2 ==0:
                self.b = tk.Label(self.Labelframe2, text=text[i//2],width=14)
            else:
                self.b = tk.Label(self.Labelframe2, text="",width=14)
                self.info.append(self.b)
            self.b.configure(activebackground="#f9f9f9")
            self.b.configure(activeforeground="black")
            self.b.configure(background="#d9d9d9")
            self.b.configure(disabledforeground="#a3a3a3")
            self.b.configure(relief="ridge")
            self.b.configure(foreground="#000000")
            self.b.configure(highlightbackground="#d9d9d9")
            self.b.configure(highlightcolor="black")
            self.b.grid(row=i//8, column=i%8)

        row = i//8


        self.Labelframe2b = tk.LabelFrame(top)
        self.Labelframe2b.place(relx=0.079, rely=0.26, relheight=0.1
                , relwidth=0.85)
        self.Labelframe2b.configure(relief='groove')
        self.Labelframe2b.configure(foreground="black")
        self.Labelframe2b.configure(text='''Symbol Ratings''')
        self.Labelframe2b.configure(background="#d9d9d9")

        sample = [{'date': 'Oct-26-20', 'category': 'Resumed','analyst': 'Atlantic Equities','rating': 'Overweight','price_from': 0.0,'price_to': 150.0}, {'date': 'Sep-21-20',
'category': 'Reiterated',
  'analyst': 'Citigroup',
  'rating': 'Buy',
  'price_from': 112.5,
  'price_to': 125.0},
 {'date': 'Sep-17-20',
  'category': 'Reiterated',
  'analyst': 'Jefferies',
  'rating': 'Buy',
  'price_from': 116.25,
  'price_to': 135.0},
 {'date': 'Sep-16-20',
  'category': 'Reiterated',
  'analyst': 'Needham',
  'rating': 'Buy',
  'price_from': 112.5,
  'price_to': 140.0},
 {'date': 'Sep-14-20',
  'category': 'Reiterated',
  'analyst': 'Oppenheimer',
  'rating': 'Outperform',
  'price_from': 105.0,
  'price_to': 125.0}]

        # row +=1
        # for i in sample:
        #     te = "{}{}{}{}{}{}{}{}".format(i["date"],i["analyst"],"rating:",i["rating"],"from",i["price_from"],"to",i["price_to"])
        #     self.b = tk.Label(self.Labelframe2, text=te,justify="left",width=50, anchor="w")
        #     self.b.configure(activebackground="#f9f9f9")
        #     self.b.configure(activeforeground="black")
        #     self.b.configure(background="#d9d9d9")
        #     self.b.configure(disabledforeground="#a3a3a3")
        #     #self.b.configure(relief="ridge")
        #     self.b.configure(foreground="#000000")
        #     self.b.configure(highlightbackground="#d9d9d9")
        #     self.b.configure(highlightcolor="black")
        #     self.b.grid(sticky = "w",row=row+1,padx=5)
        #     row +=1


        # for i in range(len(text)):
        #     self.label1 = tk.Label(self.Labelframe2 ,text=text[i],width=8)

        #     self.label1.configure(activebackground="#f9f9f9")
        #     self.label1.configure(activeforeground="black")
        #     self.label1.configure(background="yellow")
        #     self.label1.configure(disabledforeground="#a3a3a3")
        #     self.label1.configure(relief="ridge")
        #     self.label1.configure(foreground="#000000")
        #     self.label1.configure(highlightbackground="#d9d9d9")
        #     self.label1.configure(highlightcolor="black")
        #     self.label1.grid(row=i//2, column=i*2,padx=5)
        # # s= ''
        # t= '00.00'
        # text =  "Symbol: {}    Last Price: {}    \n Weekly Volitality: {}%  Monthly Volitality: {}%".format(s, t,t,t)

        # self.Labels = tk.Label(self.Labelframe2)
        # self.Labels.place(relx=0.011, rely=0.476#, #height=21 #width=104
        #         , bordermode='ignore')
        # self.Labels.configure(background="#d9d9d9")
        # self.Labels.configure(disabledforeground="#a3a3a3")
        # self.Labels.configure(foreground="#000000")
        # self.Labels.configure(text=text)


        self.Labelframe3 = tk.LabelFrame(top)
        self.Labelframe3.place(relx=0.079, rely=0.38, relheight=0.598
                , relwidth=0.852)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Options''')
        self.Labelframe3.configure(background="#d9d9d9")

        labels = ["Expiry Date", "Days left","67% confidence range", "Strike","Bid","95% confidence range", "Strike","Bid", "Most Open Interest"]

        width = [12,6,18,8,8,18,8,8,25]


        for i in range(len(labels)):
            self.label1 = tk.Label(self.Labelframe3 ,text=labels[i],width=width[i])

            self.label1.configure(activebackground="#f9f9f9")
            self.label1.configure(activeforeground="black")
            self.label1.configure(background="yellow")
            self.label1.configure(disabledforeground="#a3a3a3")
            self.label1.configure(relief="ridge")
            self.label1.configure(foreground="#000000")
            self.label1.configure(highlightbackground="#d9d9d9")
            self.label1.configure(highlightcolor="black")
            self.label1.grid(row=1, column=i,padx=5)


    def loadoptions(self,symbol,price_1,price_2,cur_price):

        df = get_all_options(symbol,self)
        dates = df.expiration.unique()
        dates_count= days_counter(dates)

        list1,list2 = report(dates,dates_count,price_1,price_2,df)

        width = [12,6,18,8,8,18,8,8,25]

        oi = most_oi(df,dates)
        oi = oi_str(oi)
        puts = np.array(list1).T[0]
        ask = np.array(list1).T[1]

        puts2 = np.array(list2).T[0]
        ask2 = np.array(list2).T[1]

        label = [dates,dates_count,price_1,puts,ask,price_2,puts2,ask2,oi]

        for j in range(len(dates)):
            self.display.append([])
            for i in range(len(label)):
                if (i != len(label)-1):
                    self.display[j].append(tk.Label(self.Labelframe3 ,text=label[i][j],width=width[i]))
                    self.display[j][i].configure(activebackground="#f9f9f9")
                    self.display[j][i].configure(activeforeground="black")
                    self.display[j][i].configure(background="#d9d9d9")
                    self.display[j][i].configure(disabledforeground="#a3a3a3")
                    self.display[j][i].configure(relief="ridge")
                    self.display[j][i].configure(foreground="#000000")
                    self.display[j][i].configure(highlightbackground="#d9d9d9")
                    self.display[j][i].configure(highlightcolor="black")
                    self.display[j][i].grid(row=j+2, column=i,padx=5)
                else:
                    self.display[j].append(tk.Button(self.Labelframe3 ,text=label[i][j],width=width[i],command=lambda k=j : self.gragh_oi(df,dates[k],cur_price,price_1[k][0],price_2[k][0])))
                    self.display[j][i].configure(activebackground="#f9f9f9")
                    self.display[j][i].configure(activeforeground="black")
                    self.display[j][i].configure(background="#d9d9d9")
                    self.display[j][i].configure(disabledforeground="#a3a3a3")
                    self.display[j][i].configure(relief="raised")
                    self.display[j][i].configure(foreground="#000000")
                    self.display[j][i].configure(highlightbackground="#d9d9d9")
                    self.display[j][i].configure(highlightcolor="black")
                    self.display[j][i].grid(row=j+2, column=i,padx=5)


        self.status['text'] ="Forecasting complete."



    #1. symbol check.
    #2. send to fetch options data.
    #3. send to donwload stock data.
    #4. Stock data download -> update.
    #5. Then calculate options.
    def loadsymbol(self):


        symbol = self.Entry1.get().capitalize()

        if validity_check(symbol):

            self.Data["state"] = "disabled"
            self.status['text'] ="Downloading stock data"
            ###1. Destory other symbol. YES
            if len(self.display)>0:
                for i in self.display:
                    for j in i:
                        j.destroy()

            self.display = []


            ###2. Error Checking.
            ###3. If possible - threading.

            t1 = threading.Thread(target=database_function,args=(self,symbol),daemon=True)
            t1.start()

            self.threads.append(t1)

        else:
            self.status['text'] ="Unrecognize symbol. Please check."



        #gragh_oi(df,dates[i],cur_price,list1[i][0],list2[i][0])


    def gragh_oi(self,df,date,cur_price,level1,level2):

        print(date)

        n = df.loc[(df["expiration"]==date)&(df["type"]=="puts")&(df["strike"]<cur_price*1.2)]

        plt.figure(figsize=(12,5))
        c,b,d=plt.hist(n["strike"].astype(int),weights=n["openInterest"],bins=32,width=4,label="OpenInterest counts")

        plt.xlabel('Strike', fontsize=8)
        plt.ylabel('open interest count', fontsize=8)
        plt.xticks(b.astype(int), fontsize=7)

        plt.axvline(cur_price,linestyle="--",linewidth=4,color="c",label="current price")
        plt.axvline(level1,linestyle="--",linewidth=5,color="y",label="67% interval boundary")


        plt.axvline(level2,linestyle="--",linewidth=7,color="r",label="95% interval boundary")
        plt.legend()
        plt.show()

        #gragh_oi(df,dates[i],cur_price,list1[i][0],list2[i][0])



def database_function(UI,symbol):
    info,price_1,price_2,vol= database(symbol,900)

    cur_price = info['LastPrice'].values[0]
    symbol = info['Symbol'].values[0]
    day_vol = round(vol/np.sqrt (252),3)
    UI.Labels["text"] = " Symbol: {}    Last Price: {}    Weekly Volitality: {}%  Monthly Volitality: {}%".format(symbol, cur_price,vol,day_vol)

    #UI.status['text'] ="Downloading options data"

    #UI.loadoptions(symbol,price_1,price_2,cur_price)

    UI.Data["state"] = "normal"




if __name__ == '__main__':



    vp_start_gui()







