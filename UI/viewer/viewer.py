import tkinter as tk                     
from tkinter import ttk 
from finviz.screener import Screener
import pandas as pd
import numpy as np



class viewer:
  def __init__(self, root=None):
    self.setting = ttk.LabelFrame(root) 
    self.setting.place(relx=0.05, rely=0, relheight=0.2
                    , relwidth=0.9)

    self.tab = ttk.LabelFrame(root) 
    self.tab.place(relx=0.05, rely=0.1, relheight=0.85
                    , relwidth=0.9)

    self.refresh = ttk.Button(self.setting,  
              text ="Refresh Data",command=self.refresh).place(relx=0.85, rely=0.1, relheight=0.25
                    , relwidth=0.1)   

    self.variable = tk.StringVar(self.setting)
    self.variable.set("one") # default value

    self.w = tk.OptionMenu(self.setting, self.variable, "one", "two", "three")

    self.tkvar = tk.StringVar(self.setting)

    # Dictionary with options
    self.choices = { 'Most Active','Top Gainner','New Highs'}
    self.tkvar.set('Most Active') # set the default option

    self.popupMenu = tk.OptionMenu(self.setting, self.tkvar, *self.choices)
    self.setting = ttk.Label(self.setting, text="Select filtering type").grid(row = 1, column = 1)
    self.popupMenu.grid(row = 2, column =1)

    self.tabControl = ttk.Notebook(self.tab) 
      
    self.tab1 = tk.Canvas(self.tabControl) 
    self.tab2 = tk.Canvas(self.tabControl) 
    self.tab3 = tk.Canvas(self.tabControl) 
      
    self.tabControl.add(self.tab1, text ='Nasdaq') 
    self.tabControl.add(self.tab2, text ='NYSE') 
    self.tabControl.add(self.tab3, text ='AMEX') 
    self.tabControl.pack(expand = 1, fill ="both") 


    labels = ["Symbol","Rel.V","Price","Change","Perf Week","MCap","Inst own",\
    "Inst tran","Insi own","Insi tran","Short float","Short Ratio","Prem Low","Prem high","Prem Avg","Status"]
    width = [8,6,6,6,8,8,8,8,8,8,10,10,10,10,10,10]

    self.info_nas = []
    self.info_nyse = []
    self.info_amex = []
    for i in range(len(labels)): #Rows
        self.b = tk.Button(self.tab1, text=labels[i],width=width[i],command=self.rank)
        self.b.configure(activebackground="#f9f9f9")
        self.b.configure(activeforeground="black")
        self.b.configure(background="#d9d9d9")
        self.b.configure(disabledforeground="#a3a3a3")
        self.b.configure(relief="ridge")
        self.b.configure(foreground="#000000")
        self.b.configure(highlightbackground="#d9d9d9")
        self.b.configure(highlightcolor="black")
        self.b.grid(row=1, column=i)

  def refresh(self):
    refreshNasdaq()
    d= readNasdaq()

    labels = ["Symbol","Rel.V","Price","Change","Perf Week","MCap","Inst own",\
    "Inst tran","Insi own","Insi tran","Short float","Short Ratio","Prem Low","Prem high","Prem Avg","Status"]
    width = [8,6,6,6,8,8,8,8,8,8,10,10,10,10,10,10]

    #append it to the view.
    for i in range(len(d)):
      info = [d.iloc[i]["Ticker"],d.iloc[i]["Rel Volume"],d.iloc[i]["Price_x"],d.iloc[i]["Change_x"],\
      d.iloc[i]["Perf Week"],d.iloc[i]["Market Cap"],d.iloc[i]["Inst Own"],d.iloc[i]["Inst Trans"],\
      d.iloc[i]["Insider Own"],d.iloc[i]["Insider Trans"],d.iloc[i]["Float Short"],d.iloc[i]["Short Ratio"],"","","",""]
      self.info_nas.append([])
      for j in range(len(labels)):
        self.info_nas[i].append(tk.Label(self.tab1 ,text=info[j],width=width[j]))
        self.info_nas[i][j].configure(activebackground="#f9f9f9")
        self.info_nas[i][j].configure(activeforeground="black")
        self.info_nas[i][j].configure(background="#d9d9d9")
        self.info_nas[i][j].configure(disabledforeground="#a3a3a3")
        self.info_nas[i][j].configure(relief="ridge")
        self.info_nas[i][j].configure(foreground="#000000")
        self.info_nas[i][j].configure(highlightbackground="#d9d9d9")
        self.info_nas[i][j].configure(highlightcolor="black")
        self.info_nas[i][j].grid(row=i+2, column=j,padx=0)

  def rank(self):
    for i in range(len(self.info_nas)):
      for j in range(len(self.info_nas[i])):
        self.info_nas[i][j].grid(row=len(self.info_nas)-i+1, column=j,padx=0)

    #add it to it .


  

def refreshNasdaq():
  filters = ['exch_nasd','sh_relvol_o3']  # Shows companies in NASDAQ which are in the S&P500
  signal = 'ta_mostactive'
  stock_list = Screener(filters=filters, table='Performance', signal=signal)  # Get the performance table and sort it by price ascending

  # Export the screener results to .csv
  stock_list.to_csv("NASDAQ_stock_basic.csv")

  stock_list2 = Screener(filters=filters, table='Ownership', signal=signal) #,order='-relativevolume'
  stock_list2.to_csv("NASDAQ_stock_own.csv")

def readNasdaq():
  d = pd.read_csv("NASDAQ_stock_basic.csv")
  d2 = pd.read_csv("NASDAQ_stock_own.csv")

  d = pd.merge(d, d2,on="Ticker",how="inner")
  return d



root = tk.Tk() 
root.title("Stocks Viewer") 
root.geometry("1019x1031")
root.minsize(120, 1)
root.maxsize(1500, 800)

view = viewer(root)
root.mainloop()