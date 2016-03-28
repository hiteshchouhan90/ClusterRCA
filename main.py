from unzipfiles import unzipfile
import sys
import os
from os.path import basename
import glob

print("Enter the input file name: ")
inputfilename = input() or "C:\Pradeep\Data\SDP.cab" # Adding the OR to avoid typing for now

# Here creating a new directory with the zip file name with the assumption that it will be mostly unique
# Then creating a sub-directory with the same name. This will be renamed to the ServerName since we don't have it yet

filenameonly = basename(inputfilename)
filenameonly = filenameonly[:filenameonly.find(".cab")]

# Getting the time frame of the issue
print("Enter the time frame of the issue in yyyy/mm/dd format:")
startdate = input("Start date:") or "2016/02/28"
enddate = input("End date:") or "2016/02/29"

rootdirectory = "C:/Pradeep/data/extract/" + filenameonly

if not os.path.exists(rootdirectory):
    os.makedirs(rootdirectory+ "/" + filenameonly)
else:
    os.remove(rootdirectory)

unzipfile(inputfilename, rootdirectory+ "/" + filenameonly)

# Now navigating to that directory and picking "ServerName_System_Information.txt"
# Then extracting the ServerName from it and renaming the directory

SysInfoFile = glob.glob(rootdirectory + "/" + filenameonly + "/*System_Information.txt")

# Using basename to get only the file name. Since this returns a list using [0]
# then looking for the first occurence of "_" and got the list in return
# again fetching the 0th element

FirstServerName = basename(SysInfoFile[0]).split("_",1)[0]

# Now renaming the folder using newly got ServerName

os.rename(rootdirectory+ "/" + filenameonly, rootdirectory+ "/" + FirstServerName)

# Here finding the server names based on the *cluster.log files
servernames =[]

for clusterlog in glob.glob(rootdirectory + "/" + FirstServerName + "/*_cluster.log"):
    servernames.append(basename(clusterlog).split(("."),1)[0].upper())

# Got the server names. Now checking if the corresponding folders exist
# If don't exist create it, prompt the user for the cab file


for servername in servernames:
    if os.path.exists(rootdirectory +"/" + servername.upper()):
        print("Folder " + servername + " exists. Not doing anything here")
    else:
        os.makedirs(rootdirectory+ "/" + servername.upper())
        print("Enter the path of the new zip file for server: " + servername.upper())
        inputfilename = input() or "C:\Pradeep\Data\SDP2.cab"
        unzipfile(inputfilename, rootdirectory + "/" + servername.upper())

print("All files extracted")

# Now creating the output file to which will contain all the data generated from now on
# adding encoding="utf-16" because while writing to the file, it was failing with the following error
# outputfile.write(line)
#   TypeError: a bytes - like object is required, not 'str'

outputfile = open(rootdirectory + "/finaloutput.txt","w", encoding="utf-16")

# Reading System Information file here
# In order to avoid reading the file multiple times creating a list of values that we need

sysinfolist =["Host Name:", "OS Name:", "System Boot Time:", "System Manufacturer:","System Model:",
              "System Type:", "Processor(s):", "BIOS Version:", "Time Zone:", "Total Physical Memory:",
              "Available Physical Memory:", "Virtual Memory: Max Size:", "Virtual Memory: Available:"]

# Now reading the file after scanning for System_Information.txt

for servername in servernames:
    outputfile.write("~"*20+"\n" + "Details of: " + servername + "\n"+ "~"*20 + "\n")
    sysinfofile = glob.glob(rootdirectory + "/" + servername.upper() + "\*System_Information.txt")[0]


# adding encoding ='utf-16' because with normal OPEN, each word would have an extra space between characters
# e.g. HOSTNAME would come out as H O S T N A M E. This was causing the IN statement to never execute!

    with open(sysinfofile, "r", encoding="utf-16") as file:
        for line in file:
            for item in sysinfolist:
                if item in line:
                    outputfile.write(line)
    outputfile.write("\n"*2)

# Here getting the SQL Server information from the ERRORLOG file
# Also creating a ignore list for removing noise from the output

    ErrorLogIgnoreList = ["(c) Microsoft Corporation", "All rights reserved.", "Server process ID is",
                          "System Manufacturer:", "Authentication mode is", "The service account is",
                          "This instance of SQL Server last reported using", "Using dynamic lock allocation",
                          "Software Usage Metrics", "Starting up database", "CLR version",
                          "finished without errors on", "Resource governor reconfiguration succeeded.",
                          "SQL Server Audit", "was started by login", "Common language runtime (CLR) functionality initialized using"
                          ]

    outputfile.write("~"*20+"\n" + "SQL Server Details: " + servername + "\n"+ "~"*20 + "\n" * 2)

# Using a list to save lines up to NETBIOS name. Then removing with the lines with words in IgnoreList
# This surely needs improvement

    trimmedlog =[]
    errorlogs = glob.glob(rootdirectory + "/" + servername.upper() + "\*_ERRORLOG")
    for errorlog in errorlogs:
        with open(errorlog,"r", encoding="utf-16") as InstanceDetails:
            for line in InstanceDetails:
                trimmedlog.append(line)
                if "Server name is " in line:
                        break
        outputfile.write("\n" * 2)

# Now removing the lines which contain the words from the IgnoreList
        for line in trimmedlog:

            for item in ErrorLogIgnoreList:
                if item in line:
                    trimmedlog.remove(line)

# Now printing the items in the trimmedlog list.
        for line in trimmedlog:
            outputfile.write(line)
        outputfile.write("\n" * 2)

# Closing the output file
outputfile.close()
