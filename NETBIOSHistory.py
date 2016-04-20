import sys
import os
import glob
from os.path import basename
import csv
from datetime import datetime

def GetNETBIOSHistory(rootdirectory, servernames,outputfile):

    """
    This module gets us the Owner of the ClusterResource by looking for NETBIOS name in the ErrorLog
    Useful when finding the history of Cluster resource ownership
    Using the start variable in such a way that if it is 1, start writing to the output file, if 0 stop
    NETBIOS name of the owner node is printed only once in the error log
    
    """
    for servername in servernames:
        ErrorLogFiles = glob.glob(rootdirectory + "/" + servername.upper() + "\*_ERRORLOG*")
        InstanceName =[]
        for item in ErrorLogFiles:
            basefile = basename(item)
            i = str(basefile).split("_")
            InstanceName.append(i[1])

        InstanceNameSet = set(InstanceName)
        for l in InstanceNameSet:
            outputfile.write("~" * 20 + "\n" + "NETBIOS name history for " + l + " instance \n" + "~" * 20 + "\n" * 2)
            ErrorLogFiles = glob.glob(rootdirectory + "/" + servername.upper() + "\*_" + l  +"*_ERRORLOG*")
            for ErrorLog in ErrorLogFiles:
                with open(ErrorLog, "r", encoding="utf-16") as ErrorLogRead:
                    start = 0
                    for line in ErrorLogRead:
                        if "The NETBIOS name of the local node that is running the server is" in line:
                            start = 1
                        else:
                            start = 0
                        if start == 1:
                            outputfile.write(line)
    outputfile.write("\n")
    print("Got NETBIOS history")