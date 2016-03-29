from SystemInfo import GetSysInfo
from unzipfiles import unzipfile
from SQLServerInfo import GetSQLInfo
from FLTMC import GetFLTMC
from Hotfix import GetHotFix
import CreateFolders
import sys
import os
import time
from os.path import basename

import glob

start_time = time.time()

print("Enter the input file name: ")
inputfilename = input() or "C:\Pradeep\Data\SDP.cab" # Adding the OR to avoid typing for now

filenameonly = basename(inputfilename)
filenameonly = filenameonly[:filenameonly.find(".cab")]

# Getting the time frame of the issue
print("Enter the time frame of the issue in yyyy/mm/dd format:")
startdate = input("Start date:") or "2016/02/28"
enddate = input("End date:") or "2016/02/29"

rootdirectory = "C:/Pradeep/data/extract/" + filenameonly

FirstServerName= CreateFolders.CreateFirstFolder(inputfilename, filenameonly, rootdirectory)
servernames= CreateFolders.CreateNextFolders(rootdirectory, FirstServerName, filenameonly)

# Now creating the output file to which will contain all the data generated from now on
# adding encoding="utf-16" because while writing to the file, it was failing with the following error
# outputfile.write(line)
#   TypeError: a bytes - like object is required, not 'str'

outputfile = open(rootdirectory + "/finaloutput.txt","w", encoding="utf-16")

GetSysInfo(rootdirectory, servernames,outputfile)
GetSQLInfo(rootdirectory, servernames,outputfile)
GetFLTMC(rootdirectory, servernames,outputfile)
GetHotFix(rootdirectory, servernames,outputfile)

# Closing the output file
print("All done.. Closing the output file")
outputfile.close()
print("--- %s seconds ---" % round((time.time() - start_time),2))