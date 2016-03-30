import sys
import os
import glob
import re
from datetime import datetime

"""
    Definition::
        Prints the filter drivers loaded on the servers
        Excludes known Microsoft filters
"""

def GetSystemLog(rootdirectory, servernames,outputfile,startdate, enddate):
    SystemLogIgnoreList = ["entered the running state", "entered the stopped state."]

# First converting the date time to match the System Event Log format i.e. 01/26/2016 05:14:34 AM
    startdate = startdate.strftime("%m/%d/%Y %I:%M:%S %p")
    enddate = enddate.strftime("%m/%d/%Y %I:%M:%S %p")

    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "System Event Log of " + servername + "\n" + "~" * 20 + "\n" * 2)
        SystemEventLog = glob.glob(rootdirectory + "/" + servername.upper() + "\*_evt_System.txt")[0]

        with open(SystemEventLog, "r", encoding="utf-8") as SysEvtLog:
            start = 0
            for line in SysEvtLog:
                if line[0].isdigit():
                    if datetime.strptime(line[:22], "%m/%d/%Y %I:%M:%S %p") >= datetime.strptime(startdate, "%m/%d/%Y %I:%M:%S %p"):
                        start = 1
                    if datetime.strptime(line[:22], "%m/%d/%Y %I:%M:%S %p") > datetime.strptime(enddate, "%m/%d/%Y %I:%M:%S %p"):
                        start = 0
                    if start == 1:
                        if not any(item in line for item in SystemLogIgnoreList):
                            outputfile.write(line)
        outputfile.write("\n" * 2)


print("Got the filter driver information\n")