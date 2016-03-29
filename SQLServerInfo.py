"""
    Definition::
        Loops through the server names
        Writes the SQL Server information (top few lines) to the output file after removing the words in the IgnoreList
        Adding encoding ='utf-16' because with normal OPEN, each word would have an extra space between characters
        HOSTNAME would come out as H O S T N A M E. This was causing the IN statement to never execute!
"""

import sys
import os
import glob

def GetSQLInfo(rootdirectory, servernames,outputfile):
    ErrorLogIgnoreList = ["(c) Microsoft Corporation", "All rights reserved.", "Server process ID is",
                          "System Manufacturer:", "Authentication mode is", "The service account is",
                          "This instance of SQL Server last reported using", "Using dynamic lock allocation",
                          "Software Usage Metrics", "Starting up database", "CLR version",
                          "finished without errors on", "Resource governor reconfiguration succeeded.",
                          "SQL Server Audit", "was started by login",
                          "Common language runtime (CLR) functionality initialized using"
                          ]
    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "SQL Server Details: " + servername + "\n" + "~" * 20 + "\n" * 2)
        trimmedlog = []
        errorlogs = glob.glob(rootdirectory + "/" + servername.upper() + "\*_ERRORLOG")
        for errorlog in errorlogs:
            with open(errorlog, "r", encoding="utf-16") as InstanceDetails:
                for line in InstanceDetails:
                    #trimmedlog.append(line)
                    if not any(item in line for item in ErrorLogIgnoreList):
                        outputfile.write(line)
                    if "The NETBIOS name of the local node" in line:
                        break
            outputfile.write("\n" * 2)

            # for line in trimmedlog:
            #
            #     for item in ErrorLogIgnoreList:
            #         if item in line:
            #             trimmedlog.remove(line)
            #
            #             # Now printing the items in the trimmedlog list.
            # for line in trimmedlog:
            #     outputfile.write(line)

        print("Got ERROR LOG for " + servername.upper())
