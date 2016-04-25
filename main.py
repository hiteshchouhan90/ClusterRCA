import msvcrt
import fnmatch
from ClusterLogParser import ClusterLogParser
from SystemInfo import GetSysInfo
from SQLServerInfo import GetSQLInfo
from FLTMC import GetFLTMC
from Hotfix import GetHotFix
from SystemEventLog import GetSystemLog
from NETBIOSHistory import GetNETBIOSHistory
from StorNetDrivers import GetStorageNetworkDrivers
from ClusterDependencies import GetClusterDependencies
import CreateFolders
import os
import time
from datetime import datetime, timedelta
from os.path import basename
from SQLErrorLogParser import SQLErrorLogParser


print("Enter the input file name: ")
inputfilename = input() or "C:\ClusterRCA\DB01.cab" # Adding the OR to avoid typing for now

filenameonly = basename(inputfilename)
filenameonly = filenameonly[:filenameonly.find(".cab")]

# Getting the time frame of the issue
print("Enter the time frame of the issue in \"yyyy/mm/dd HH:mm\" format:")
startdate = input("Start date:\n") or "2016/02/23 09:00"
enddate = input("End date:\n") or "2016/02/23 11:00"

# Adding/subtracting  two hours as buffer

startdate = datetime.strptime(startdate, "%Y/%m/%d %H:%M") - timedelta(hours=2)
enddate = datetime.strptime(enddate, "%Y/%m/%d %H:%M") + timedelta(hours=2)


start_time = time.time()
rootdirectory = "C:/ClusterRCA" + "/" + filenameonly

FirstServerName= CreateFolders.CreateFirstFolder(inputfilename, filenameonly, rootdirectory)
servernames= CreateFolders.CreateNextFolders(rootdirectory, FirstServerName, filenameonly)

# Now creating the output file to which will contain all the data generated from now on
# adding encoding="utf-16" because while writing to the file, it was failing with the following error
# outputfile.write(line)
#   TypeError: a bytes - like object is required, not 'str'

outputfile = open(rootdirectory + "/finaloutput.txt","w", encoding="utf-16")



#getting instance names for servers --


instancename=[]
for servername in servernames:
    for file in os.listdir(rootdirectory+ '/'+ servername):
        #print(file)
        if fnmatch.fnmatch(file,'*ERRORLOG*'):
            #print(file)
            file=file.split('_')
            instancename.append(file[1])
            #print(instancename)
    #        instancename=set(file[1])
instancename=set((instancename))
instancename=list(instancename)


GetSysInfo(rootdirectory, servernames,outputfile)
#GetSQLInfo(rootdirectory, servernames,outputfile)
GetFLTMC(rootdirectory, servernames,outputfile)
GetStorageNetworkDrivers(rootdirectory, servernames,outputfile)
GetHotFix(rootdirectory, servernames,outputfile)
GetClusterDependencies(rootdirectory, servernames,outputfile)
GetNETBIOSHistory(rootdirectory, servernames,outputfile)
GetSystemLog(rootdirectory, servernames,outputfile,startdate, enddate)
SQLErrorLogParser(startdate,enddate,rootdirectory,servernames,instancename,outputfile)
ClusterLogParser(rootdirectory,servernames,outputfile,startdate,enddate)

print("All done.. Closing the output file\n")
outputfile.close()

print("Output file can be found at " + str(outputfile.name).replace("/","\\")+ "\n")
while True:
    user_input = input("Hit ENTER to quit:\n")
    if user_input == "":
        break
