import tkinter as tk

window = tk.Tk()

greeting = tk.Label(
    text="Hello, Tkinter",
    foreground="white",  # Set the text color to white
    background="black", # Set the background color to black
    width=10,
    height=10
)
button = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
)
# frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
# frame1.pack()
# frame2 = tk.Frame(master=window, width=100, height=100, bg="blue")
# frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
# frame3 = tk.Frame(master=window, width=100, height=100, bg="yellow")
# frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

# entry = tk.Entry(fg="yellow", bg="blue", width=50)
# text_box = tk.Text()
# text_box.pack()
# entry.pack()
# greeting.pack()
# button.pack()

# label1X = tk.Label(master=frame2, text="I'm at (0, 0)", bg="red")
# label1X.place(x=0, y=0)

for i in range(3):
    for j in range(3):
        frame = tk.Frame(
            master=window,
            width=100, height=100,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=i, column=j)
        label = tk.Label(master=frame, text=f"Row {i}\nColumn {j}")
        label.pack()
window.mainloop()