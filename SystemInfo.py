"""
    Definition::
        Loops through the server names
        Writes the System Information to the output file after removing the words in the IgnoreList
        Adding encoding ='utf-16' because with normal OPEN, each word would have an extra space between characters
        HOSTNAME would come out as H O S T N A M E. This was causing the IN statement to never execute!
"""
import sys
import os
import glob

def GetSysInfo(rootdirectory, servernames,outputfile):

    sysinfolist = ["Host Name:", "OS Name:", "System Boot Time:", "System Manufacturer:", "System Model:",
                   "System Type:", "Processor(s):", "BIOS Version:", "Time Zone:", "Total Physical Memory:",
                   "Available Physical Memory:", "Virtual Memory: Max Size:", "Virtual Memory: Available:"]

    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "Details of: " + servername + "\n" + "~" * 20 + "\n")
        sysinfofile = glob.glob(rootdirectory + "/" + servername.upper() + "\*System_Information.txt")[0]

        with open(sysinfofile, "r", encoding="utf-16") as file:
            for line in file:
                for item in sysinfolist:
                    if item in line:
                        outputfile.write(line)
        outputfile.write("\n" * 2)
        print("Got System Information for " + servername.upper())
