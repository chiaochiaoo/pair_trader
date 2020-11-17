from tkinter import*
import numpy as np
import matplotlib.pyplot as plt
#import Database

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure


# root = tkinter.Tk()
# root.wm_title("Embedding in Tk")

# fig = Figure(figsize=(5, 4), dpi=100)
# t = np.arange(0, 3, .01)
# fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

# canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
# canvas.draw()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# def on_key_press(event):
#     print("you pressed {}".format(event.key))
#     key_press_handler(event, canvas, toolbar)


# canvas.mpl_connect("key_press_event", on_key_press)


# def _quit():
#     root.quit()     # stops mainloop
#     root.destroy()  # this is necessary on Windows to prevent
#                     # Fatal Python Error: PyEval_RestoreThread: NULL tstate


# button = tkinter.Button(master=root, text="Quit", command=_quit)
# button.pack(side=tkinter.BOTTOM)

# tkinter.mainloop()

class MyWindow:
    def __init__(self, win):


        # win.columnconfigure(0, pad=3)
        # win.columnconfigure(1, pad=3)
        # win.columnconfigure(2, pad=3)
        # win.columnconfigure(3, pad=3)

        # win.rowconfigure(0, pad=3)
        # win.rowconfigure(1, pad=3)
        # win.rowconfigure(2, pad=3)
        # win.rowconfigure(3, pad=3)
        # win.rowconfigure(4, pad=3)

        self.lbl1=Label(win, text='Symbol')
        self.lbl1.place(x=50, y=50)
        self.lbl1.grid(row=0, column=0,rowspan=2)

        self.t1=Entry(bd=3)
        self.t1.place(x=100, y=50)
        self.t1.grid(row=0, column=1)


        self.b1=Button(win, text='load', command=self.load)
        self.b1.place(x=250, y=50)
        self.b1.grid(row=0, column=2)

        self.lbl=Label(win, text="")
        self.lbl.place(x=100, y=100)
        self.lbl.grid(row=0, column=3)


        self.frame = Frame(win,height=500, width = 500)
        self.frame.place(x=25, y=50)
        #self.frame.pack(side=LEFT, expand = 1, pady = 50, padx = 50)

        labels = ["Date", "67% inteval", "95% interval", "Strike within 67%", "Strike between 67% and 95%"]

        for j in range(30):
            for i in range(len(labels)):
                label1 = Label(self.frame ,text=labels[i])
                label1.grid(row=j, column=i,padx=5)

    def load(self):
        self.lbl['text']=("sfsfsf")
        plt.plot([1,2,3],[1,2,3])
        plt.show()


window=Tk()
mywin= MyWindow(window)
window.title('Options Selector')
window.geometry("600x300+10+10")
window.mainloop()