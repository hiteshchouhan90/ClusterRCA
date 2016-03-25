from unzipfiles import unzipfile
import sys
import os
from os.path import basename
import glob

print("Enter the input file name: ")
inputfilename = input()

# Here creating a new directory with the zip file name with the assumption that it will be mostly unique
# Then creating a sub-directory with the same name. This will be renamed to the ServerName since we don't have it yet

filenameonly = basename(inputfilename)
filenameonly = filenameonly[:filenameonly.find(".cab")]

rootdirectory = "C:/Pradeep/data/extract/" + filenameonly

if not os.path.exists(rootdirectory):
    os.makedirs(rootdirectory+ "/" + filenameonly)

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
        inputfilename = input()
        unzipfile(inputfilename, rootdirectory + "/" + servername.upper())

print("All files extracted")

# Now creating the output file to which will contain all the data generated from now on
# adding encoding="utf-16" because while writing to the file, it would fail with the following error
# outputfile.write(line)
#   TypeError: a bytes - like object is required, not 'str'

outputfile = open(rootdirectory + "/finaloutput.txt","w", encoding="utf-16")

# Reading System Information file here
# In order to avoid reading the file multiple times creating a list of values that we need

sysinfolist =["Host Name:", "OS Name:", "System Boot Time:", "System Manufacturer:","System Model:"\
              "System Type:", "Processor(s):", "BIOS Version:", "Time Zone:", "Total Physical Memory:" \
              "Available Physical Memory:", "Virtual Memory: Max Size:", "Virtual Memory: Available:"]

# Now reading the file after scanning for System_Information.txt

for servername in servernames:
    outputfile.write("Details of: " + servername + "\n"*2)
    sysinfofile = glob.glob(rootdirectory + "/" + servername.upper() + "\*System_Information.txt")[0]


# adding encoding ='utf-16' because with normal OPEN, each word would have an extra space between characters
# e.g. HOSTNAME would come out as H O S T N A M E. This was causing the IN statement to never execute!

    with open(sysinfofile, "r", encoding="utf-16") as file:
        for line in file:
            for item in sysinfolist:
                if item in line:
                    outputfile.write(line)
    outputfile.write("\n"*2)
print("System Information printed")
# Closing the output file
outputfile.close()
