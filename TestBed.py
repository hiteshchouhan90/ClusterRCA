import sys, glob, os
from itertools import islice
from operator import itemgetter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from datetime import date


def load_file():
    fname = askopenfilename(filetypes=[("Cabinet files", "*.cab")])
    if fname:
        try:
            print("Got the file :" + fname)
        except:  # <- naked except is a bad idea
            showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        return

top = Tk()


lblinput = Label(top, text="Enter file name here")
lblyear = Label(top, text="Year:")
lblMonth = Label(top, text="Month:")
lblDate = Label(top, text="Date:")
lblHour = Label(top, text="Hour:")

entryinput = Entry(top)

browsebutton = Button(text="Browse", command=load_file, width=10)

# Creating date and time picker here
yearval = StringVar(top)
monthval = StringVar(top)
dateval = StringVar(top)
timeval = StringVar(top)

# Getting the current year and -1
yearlist = []
yearlist.append(date.today().year)
yearlist.append(date.today().year-1)

yearbtn = OptionMenu(top, yearval, *yearlist)
monthbtn = OptionMenu(top, monthval, *list(range(1,13)  ))
datebtn = OptionMenu(top, dateval, *list(range(1,32)  ) )
timebtn = OptionMenu(top, timeval, *list(range(1,25)  ) )
# Aligning the user controls here
inputframe = Frame(top)
#inputframe.pack(fill=X, side=BOTTOM)
inputframe.columnconfigure(0, weight=1)
inputframe.columnconfigure(1, weight=1)
inputframe.columnconfigure(2, weight=1)
inputframe.columnconfigure(3, weight=1)
inputframe.columnconfigure(4, weight=1)
inputframe.columnconfigure(5, weight=1)
inputframe.columnconfigure(6, weight=1)

lblinput.grid(row=0, column=0)
entryinput.grid(row=0, column=1)
browsebutton.grid(row=0, column=2)
lblyear.grid(row=3, column=0)
yearbtn.grid(row=3, column=1)
lblMonth.grid(row=3, column=2)
monthbtn.grid(row=3, column=3)
lblDate.grid(row=3, column=4)
datebtn.grid(row=3, column=5)
lblHour.grid(row=3, column=6)
timebtn.grid(row=3, column=7)

top.mainloop()