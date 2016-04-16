import sys
import os
import glob
import re
import csv
from datetime import datetime

"""
    Definition::
        Prints the filter drivers loaded on the servers
        Excludes known Microsoft filters
"""

def Tabs(TextInput):
    n= round(40-len(TextInput)/8)
    Tabs = "\t" * n
    return Tabs

# I will call the above function Tabs later
# For now leaving the output formatting as it is

def GetSystemLog(rootdirectory, servernames,outputfile,startdate, enddate):
    SystemLogIgnoreList = ["entered the running state", "entered the stopped state."]

# First converting the date time to match the System Event Log format i.e. 01/26/2016 05:14:34 AM
    startdate = startdate.strftime("%m/%d/%Y %I:%M:%S %p")
    enddate = enddate.strftime("%m/%d/%Y %I:%M:%S %p")

    convertedStartDate = datetime.strptime(startdate, "%m/%d/%Y %I:%M:%S %p")
    convertedEndDate = datetime.strptime(enddate, "%m/%d/%Y %I:%M:%S %p")
    for servername in servernames:
        lastline = ""
        similarlinecount = 0

        outputfile.write("~" * 20 + "\n" + "System Event Log of " + servername + "\n" + "~" * 20 + "\n" * 2)
        SystemEventLog = glob.glob(rootdirectory + "/" + servername.upper() + "\*_evt_System.csv")[0]
        with open(SystemEventLog, "r", encoding="utf-8") as SysEvtLog:
            SystemCSV = csv.reader(SysEvtLog, delimiter=',')
            start = 0
            for line in SystemCSV:
                if len(line[0])>=10:
                    if line[0][0].isdigit():
                        if datetime.strptime(line[0] +" " + line[1], "%m/%d/%Y %I:%M:%S %p") >= convertedStartDate:
                            start = 1
                        if datetime.strptime(line[0] +" " + line[1], "%m/%d/%Y %I:%M:%S %p") > convertedEndDate:
                            start = 0
                        if start == 1:
                            if not any(item in line[8] for item in SystemLogIgnoreList):
                                if line[8] == lastline:
                                    similarlinecount += 1
                                else:
                                    if similarlinecount == 0:
                                        outputfile.write(line[0] + " " + line[1] + "\t" + line[2] + "\t" + line[5] + "\t" + line[8] + "\n")
                                    else:
                                        outputfile.write("\t"* 4 + "~~~~  Above message appears " + str(similarlinecount) + " times  ~~~~" +"\n"*2)
                                    similarlinecount = 0

                                lastline = line[8]
        outputfile.write("\n" * 2)


    print("Got the System Event Log")