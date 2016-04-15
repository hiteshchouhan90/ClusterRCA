import pyunpack
import glob
from os.path import basename
from unzipfiles import unzipfile

from SystemInfo import GetSysInfo
from unzipfiles import unzipfile
from SQLServerInfo import GetSQLInfo
from FLTMC import GetFLTMC
from Hotfix import GetHotFix
from SystemEventLog import GetSystemLog
from NETBIOSHistory import GetNETBIOSHistory
from StorNetDrivers import GetStorageNetworkDrivers
from ClusterDependencies import GetClusterDependencies
from SP_Configure import GetSPConfigure
import CreateFolders
import sys
import os
import time
from datetime import datetime, timedelta
from os.path import basename


import glob



print("Enter the input file name: ")
inputfilename = input() or "C:\Pradeep\Data\SDP.cab" # Adding the OR to avoid typing for now

filenameonly = basename(inputfilename)
filenameonly = filenameonly[:filenameonly.find(".cab")]

# Getting the time frame of the issue
print("Enter the time frame of the issue in \"yyyy/mm/dd HH:mm\" format:")
startdate = input("Start date:\n") or "2016/02/21 12:21"
enddate = input("End date:\n") or "2016/02/21 14:21"

"""
Some inputs for testing

C:\Pradeep\Data\SDP_Single.cab
2016/03/20 00:00
2016/03/20 05:00
"""
# Adding/subtracting  two hours as buffer

startdate = datetime.strptime(startdate, "%Y/%m/%d %H:%M") - timedelta(hours=2)
enddate = datetime.strptime(enddate, "%Y/%m/%d %H:%M") + timedelta(hours=2)


start_time = time.time()
rootdirectory = os.getcwd() + "/" + filenameonly

FirstServerName= CreateFolders.CreateFirstFolder(inputfilename, filenameonly, rootdirectory)
servernames= CreateFolders.CreateNextFolders(rootdirectory, FirstServerName, filenameonly)

# Now creating the output file to which will contain all the data generated from now on
# adding encoding="utf-16" because while writing to the file, it was failing with the following error
# outputfile.write(line)
#   TypeError: a bytes - like object is required, not 'str'

outputfile = open(rootdirectory + "/finaloutput.txt","w", encoding="utf-16")

GetSysInfo(rootdirectory, servernames,outputfile)
GetSQLInfo(rootdirectory, servernames,outputfile)
GetSPConfigure(rootdirectory, servernames,outputfile)
GetFLTMC(rootdirectory, servernames,outputfile)
GetStorageNetworkDrivers(rootdirectory, servernames,outputfile)
GetHotFix(rootdirectory, servernames,outputfile)
GetClusterDependencies(rootdirectory, servernames,outputfile)
GetNETBIOSHistory(rootdirectory, servernames,outputfile)
sysstart = time.time()
GetSystemLog(rootdirectory, servernames,outputfile,startdate, enddate)
print("--- %s Time for SysLog ---" % round((time.time() - sysstart),2))
# Closing the output file
print("--- %s seconds ---" % round((time.time() - start_time),2))
print("All done.. Closing the output file\n")
outputfile.close()
print("Output file can be found at " + str(outputfile.name).replace("/","\\")+ "\n")
while True:
    user_input = input("Hit ENTER to quit:\n")
    if user_input == "":
        break
