#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.6
#  in conjunction with Tcl version 8.6
#    Nov 10, 2020 10:34:32 PM EST  platform: Windows NT

import sys

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

#import option_support

v = 1

choices = [
    ("Automatic",1),
    ("Regressive",2),
    ("Stationary",3),
    ("Bullish",4),
    ("Bearish",5)
]


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


  # initializing the choice, i.e. Python
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("1019x1031+836+229")
        top.minsize(120, 1)
        top.maxsize(2564, 1421)
        top.resizable(1,  1)
        top.title("New Toplevel")
        top.configure(background="#d9d9d9")

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

        self.Data = tk.Button(self.Labelframe1)
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
        self.status.place(relx=0.586, rely=0.476, height=21, width=203
                , bordermode='ignore')
        self.status.configure(background="#d9d9d9")
        self.status.configure(disabledforeground="#a3a3a3")
        self.status.configure(foreground="#000000")
        self.status.configure(text='''Status: waiting for symbol''')

        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.079, rely=0.155, relheight=0.196
                , relwidth=0.85)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Forecast Setting''')
        self.Labelframe2.configure(background="#d9d9d9")

        # self.Radiobutton1 = tk.Radiobutton(self.Labelframe2)
        # self.Radiobutton1.place(relx=0.104, rely=0.149, relheight=0.144
        #         , relwidth=0.09, bordermode='ignore')
        # self.Radiobutton1.configure(activebackground="#ececec")
        # self.Radiobutton1.configure(activeforeground="#000000")
        # self.Radiobutton1.configure(background="#d9d9d9")
        # self.Radiobutton1.configure(disabledforeground="#a3a3a3")
        # self.Radiobutton1.configure(foreground="#000000")
        # self.Radiobutton1.configure(highlightbackground="#d9d9d9")
        # self.Radiobutton1.configure(highlightcolor="black")
        # self.Radiobutton1.configure(justify='left')
        # self.Radiobutton1.configure(text='''Automatic''')
        # #self.Radiobutton1.configure(variable=option_support.selectedButton)

        # self.Radiobutton1_1 = tk.Radiobutton(self.Labelframe2)
        # self.Radiobutton1_1.place(relx=0.104, rely=0.297, relheight=0.144
        #         , relwidth=0.09, bordermode='ignore')
        # self.Radiobutton1_1.configure(activebackground="#ececec")
        # self.Radiobutton1_1.configure(activeforeground="#000000")
        # self.Radiobutton1_1.configure(background="#d9d9d9")
        # self.Radiobutton1_1.configure(cursor="fleur")
        # self.Radiobutton1_1.configure(disabledforeground="#a3a3a3")
        # self.Radiobutton1_1.configure(foreground="#000000")
        # self.Radiobutton1_1.configure(highlightbackground="#d9d9d9")
        # self.Radiobutton1_1.configure(highlightcolor="black")
        # self.Radiobutton1_1.configure(justify='left')
        # self.Radiobutton1_1.configure(text='''Regressive''')
        # #self.Radiobutton1_1.configure(variable=option_support.selectedButton)

        # self.Radiobutton1_2 = tk.Radiobutton(self.Labelframe2)
        # self.Radiobutton1_2.place(relx=0.104, rely=0.446, relheight=0.153
        #         , relwidth=0.09, bordermode='ignore')
        # self.Radiobutton1_2.configure(activebackground="#ececec")
        # self.Radiobutton1_2.configure(activeforeground="#000000")
        # self.Radiobutton1_2.configure(background="#d9d9d9")
        # self.Radiobutton1_2.configure(disabledforeground="#a3a3a3")
        # self.Radiobutton1_2.configure(foreground="#000000")
        # self.Radiobutton1_2.configure(highlightbackground="#d9d9d9")
        # self.Radiobutton1_2.configure(highlightcolor="black")
        # self.Radiobutton1_2.configure(justify='left')
        # self.Radiobutton1_2.configure(text='''Stationary''')
        # #self.Radiobutton1_2.configure(variable=option_support.selectedButton)

        # self.Radiobutton1_3 = tk.Radiobutton(self.Labelframe2)
        # self.Radiobutton1_3.place(relx=0.081, rely=0.594, relheight=0.134
        #         , relwidth=0.113, bordermode='ignore')
        # self.Radiobutton1_3.configure(activebackground="#ececec")
        # self.Radiobutton1_3.configure(activeforeground="#000000")
        # self.Radiobutton1_3.configure(background="#d9d9d9")
        # self.Radiobutton1_3.configure(disabledforeground="#a3a3a3")
        # self.Radiobutton1_3.configure(foreground="#000000")
        # self.Radiobutton1_3.configure(highlightbackground="#d9d9d9")
        # self.Radiobutton1_3.configure(highlightcolor="black")
        # self.Radiobutton1_3.configure(justify='left')
        # self.Radiobutton1_3.configure(text='''Bullish''')
        # #self.Radiobutton1_3.configure(variable=option_support.selectedButton)

        # self.Radiobutton1_3_1 = tk.Radiobutton(self.Labelframe2)
        # self.Radiobutton1_3_1.place(relx=0.092, rely=0.743, relheight=0.134
        #         , relwidth=0.09, bordermode='ignore')
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        # self.Radiobutton1_3_1.configure()
        #self.Radiobutton1_3_1.configure(variable=option_support.selectedButton)

        global v
        v = tk.IntVar()
        v.set(1)

        for val, language in enumerate(choices):
            print(val,language[0])
            self.b=tk.Radiobutton(self.Labelframe2, 
                          text=language[0],
                          padx = 20, 
                          variable=v, 
                          command=ShowChoice,
                          activebackground="#ececec",
                          activeforeground="#000000",
                          background="#d9d9d9",
                          disabledforeground="#a3a3a3",
                          foreground="#000000",
                          highlightbackground="#d9d9d9",
                          highlightcolor="black",
                          justify='left',
                          value=val)
            self.b.place(relx=0.092, rely=0.15*(val+1), relheight=0.134
                , relwidth=0.15, bordermode='ignore')


        self.Forecast = tk.Button(self.Labelframe2)
        self.Forecast.place(relx=0.762, rely=0.198, height=44, width=157
                , bordermode='ignore')
        self.Forecast.configure(activebackground="#ececec")
        self.Forecast.configure(activeforeground="#000000")
        self.Forecast.configure(background="#d9d9d9")
        self.Forecast.configure(disabledforeground="#a3a3a3")
        self.Forecast.configure(foreground="#000000")
        self.Forecast.configure(highlightbackground="#d9d9d9")
        self.Forecast.configure(highlightcolor="black")
        self.Forecast.configure(pady="0")
        self.Forecast.configure(text='''Forecast''')

        self.Forecast_1 = tk.Button(self.Labelframe2)
        self.Forecast_1.place(relx=0.762, rely=0.644, height=44, width=157
                , bordermode='ignore')
        self.Forecast_1.configure(activebackground="#ececec")
        self.Forecast_1.configure(activeforeground="#000000")
        self.Forecast_1.configure(background="#d9d9d9")
        self.Forecast_1.configure(disabledforeground="#a3a3a3")
        self.Forecast_1.configure(foreground="#000000")
        self.Forecast_1.configure(highlightbackground="#d9d9d9")
        self.Forecast_1.configure(highlightcolor="black")
        self.Forecast_1.configure(pady="0")
        self.Forecast_1.configure(text='''Chart''')

        self.regressive_input = tk.Entry(self.Labelframe2)
        self.regressive_input.place(relx=0.346, rely=0.347, height=17
                , relwidth=0.109, bordermode='ignore')
        self.regressive_input.configure(background="white")
        self.regressive_input.configure(disabledforeground="#a3a3a3")
        self.regressive_input.configure(font="TkFixedFont")
        self.regressive_input.configure(foreground="#000000")
        self.regressive_input.configure(insertbackground="black")

        self.bulish_input = tk.Entry(self.Labelframe2)
        self.bulish_input.place(relx=0.346, rely=0.644, height=17, relwidth=0.109
                , bordermode='ignore')
        self.bulish_input.configure(background="white")
        self.bulish_input.configure(disabledforeground="#a3a3a3")
        self.bulish_input.configure(font="TkFixedFont")
        self.bulish_input.configure(foreground="#000000")
        self.bulish_input.configure(highlightbackground="#d9d9d9")
        self.bulish_input.configure(highlightcolor="black")
        self.bulish_input.configure(insertbackground="black")
        self.bulish_input.configure(selectbackground="blue")
        self.bulish_input.configure(selectforeground="white")

        self.bearish_input = tk.Entry(self.Labelframe2)
        self.bearish_input.place(relx=0.346, rely=0.792, height=17
                , relwidth=0.109, bordermode='ignore')
        self.bearish_input.configure(background="white")
        self.bearish_input.configure(disabledforeground="#a3a3a3")
        self.bearish_input.configure(font="TkFixedFont")
        self.bearish_input.configure(foreground="#000000")
        self.bearish_input.configure(highlightbackground="#d9d9d9")
        self.bearish_input.configure(highlightcolor="black")
        self.bearish_input.configure(insertbackground="black")
        self.bearish_input.configure(selectbackground="blue")
        self.bearish_input.configure(selectforeground="white")

        self.Label2 = tk.Label(self.Labelframe2)
        self.Label2.place(relx=0.277, rely=0.347, height=21, width=34
                , bordermode='ignore')
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(text='''Days:''')

        self.Label2_1 = tk.Label(self.Labelframe2)
        self.Label2_1.place(relx=0.254, rely=0.644, height=21, width=73
                , bordermode='ignore')
        self.Label2_1.configure(activebackground="#f9f9f9")
        self.Label2_1.configure(activeforeground="black")
        self.Label2_1.configure(background="#d9d9d9")
        self.Label2_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1.configure(foreground="#000000")
        self.Label2_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1.configure(highlightcolor="black")
        self.Label2_1.configure(text='''Magnitude:''')

        self.Label2_1_1 = tk.Label(self.Labelframe2)
        self.Label2_1_1.place(relx=0.254, rely=0.792, height=21, width=73
                , bordermode='ignore')
        self.Label2_1_1.configure(activebackground="#f9f9f9")
        self.Label2_1_1.configure(activeforeground="black")
        self.Label2_1_1.configure(background="#d9d9d9")
        self.Label2_1_1.configure(disabledforeground="#a3a3a3")
        self.Label2_1_1.configure(foreground="#000000")
        self.Label2_1_1.configure(highlightbackground="#d9d9d9")
        self.Label2_1_1.configure(highlightcolor="black")
        self.Label2_1_1.configure(text='''Magnitude:''')

        self.Labelframe3 = tk.LabelFrame(top)
        self.Labelframe3.place(relx=0.079, rely=0.369, relheight=0.598
                , relwidth=0.852)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Options''')
        self.Labelframe3.configure(background="#d9d9d9")

if __name__ == '__main__':
    vp_start_gui()





