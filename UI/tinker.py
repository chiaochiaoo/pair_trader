# import tkinter as tk
# import pandas as pd
# import random 

# window = tk.Tk()

# window.columnconfigure([0,1,2,3,4,5,6,7,8,9], minsize=100)
# window.rowconfigure([0, 1], minsize=100)


# labels = ["Symbol", "Price", "R Vol 5 min", "R Vol 30 min", "R Vol", "Chg 5 Min(%)", "Chg 30 Min(%)", "Chg since close(%)", "Last Updated On"]


# # TOP MENU.
# for i in range(len(labels)):
# 	label1 = tk.Button(text=labels[i],width=15)
# 	label1.grid(row=0, column=i, sticky="n")


# symbols = ["AAL.NQ","XRAY.NQ","UAL.NQ","AMWL.NQ","LYFT.NQ","SEIC.NQ","FROG.NQ","YY.NQ","LNC.NQ"]




# ## THOUGHT.

# # button = tk.Button(
# #     text="Click me!",
# #     width=25,
# #     height=5,
# #     bg="blue",
# #     fg="yellow",
# # )
# # frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
# # frame1.pack()
# # frame2 = tk.Frame(master=window, width=100, height=100, bg="blue")
# # frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
# # frame3 = tk.Frame(master=window, width=100, height=100, bg="yellow")
# # frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# # entry = tk.Entry(fg="yellow", bg="blue", width=50)
# # text_box = tk.Text()
# # text_box.pack()
# # entry.pack()
# # greeting.pack()
# # button.pack()

# # label1X = tk.Label(master=frame2, text="I'm at (0, 0)", bg="red")
# # label1X.place(x=0, y=0)


# window.mainloop()


from tkinter import * 

root = Tk()

f = Frame(root, bg = "orange", width = 500, height = 500)
f.pack(side=LEFT, expand = 1)

f3 = Frame(f, bg = "red", width = 500)
f3.pack(side=LEFT, expand = 1, pady = 50, padx = 50)

f2 = Frame(root, bg = "black", height=100, width = 100)
f2.pack(side=LEFT, fill = Y)

b = Button(f2, text = "test")
b.pack()

b = Button(f3, text = "1", bg = "red")
b.grid(row=0, column=3)
b2 = Button(f3, text = "2")
b2.grid(row=1, column=4)
b3 = Button(f3, text = "2")
b3.grid(row=2, column=0)

root.mainloop()