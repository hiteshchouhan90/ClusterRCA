import sys
import os
import glob
import re

"""
    Definition::
        Prints the filter drivers loaded on the servers
        Excludes known Microsoft filters
"""

def GetFLTMC(rootdirectory, servernames,outputfile):
    FLTMCIgnoreList =["FsDepends","CsvNSFlt","CsvFlt","CCFFilter","ResumeKeyFilter","svhdxflt","luafv","npsvctrig"
                      ,"VirtFile","msnfsflt","Quota","Datascrn"]

    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "Filter Drivers loaded on " + servername + "\n" + "~" * 20 + "\n" * 2)
        FLTMCFiles = glob.glob(rootdirectory + "/" + servername.upper() + "\*_Fltmc.TXT")
        for FLTMC in FLTMCFiles:
            with open(FLTMC, "r", encoding="utf-16") as FilterDetails:
                start=0
                for line in FilterDetails:
                    if "Filter Name" in line:
                        start =1
                    if "--------------------------------------------------" in line:
                        start = 0
                    if start==1:
                        if not any (item in line for item in FLTMCIgnoreList):
                            outputfile.write(line[:46]+"\n")
        outputfile.write("\n" * 2)
    print("Got the filter driver information\n")