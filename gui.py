import sys, glob, os
from itertools import islice
from operator import itemgetter
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from datetime import date

inputfilename="a"
startdate=""
enddate=""
servername=""

def load_GUI(firstorsecond):

    """
    Here we will load the GUI
    It accepts parameter firstorsecond
    If this param is first then a first file, start and end dates are show
    If this param is second then only the file load option is shown
    """
    inputfilename="bb"
    def load_file():
        inputfilename = askopenfilename(filetypes=[("Cabinet files", "*.cab")])
        if inputfilename:
            try:
                print("Got the file :" + inputfilename)
                if firstorsecond == "first":
                    entryinput.insert(0, inputfilename)
                else:
                    secondinput.insert(0, inputfilename)
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % inputfilename)


    def callback():
        global inputfilename,startdate,enddate
        if firstorsecond == "first":
            inputfilename= entryinput.get()
            startdate = entryFrom.get()
            enddate = entryTo.get()
            top.quit()
            top.destroy()
        elif firstorsecond == "second":
            global servername
            inputfilename = secondinput.get()
            top.quit()
            top.destroy()



    top = Tk()

    if firstorsecond=="first":
        lblinput = Label(top, text="Enter file name here                          ")
        lblFrom  = Label(top, text="From date (yyyy/MM/dd HH:mm) ")
        lblTo  = Label(top, text="From date (yyyy/MM/dd HH:mm) ")

        entryinput = Entry(top)
        browsebutton = Button(text="Browse", command=load_file, width=10)

        entryFrom = Entry(top)
        entryTo = Entry(top)

        btnSubmit = Button(text='Submit', width=10, command=callback)


        # Aligning the user controls here
        inputframe = Frame(top)

        lblinput.grid(row=0, column=0)
        lblFrom.grid(row=1, column=0)
        lblTo.grid(row=2, column=0)

        entryinput.grid(row=0, column=1)
        browsebutton.grid(row=0, column=2)
        entryFrom.grid(row=1, column=1)
        entryTo.grid(row=2, column=1)

        btnSubmit.grid(row=4, column=1)
    elif firstorsecond=="second":
        print("Second")
        secondlblinput = Label(top, text="Enter the file name for " + servername +"                          ")
        secondbrowsebutton = Button(text="Browse", command=load_file, width=10)
        secondbtnSubmit = Button(text='Submit', width=10, command=callback)
        secondinput = Entry(top)

        inputframe = Frame(top)
        secondlblinput.grid(row=0, column=0)
        secondinput.grid(row=0, column=1)
        secondbrowsebutton.grid(row=0, column=2)
        secondbtnSubmit.grid(row=4, column=1)

    top.mainloop()

#load_GUI("second")
