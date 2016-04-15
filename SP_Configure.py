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

from itertools import islice

def GetSPConfigure(rootdirectory, servernames,outputfile):
    for servername in servernames:


        if len(glob.glob(rootdirectory + "/" + servername.upper() + "\*sp_sqldiag_Shutdown.OUT"))>0:
            sqldiag = glob.glob(rootdirectory + "/" + servername.upper() + "\*sp_sqldiag_Shutdown.OUT")[0]
            outputfile.write("~" * 15 + "\n" + "SQL Server Configuration Details: " + servername + "\n" + "~" * 15 + "\n" * 2)

            with open(sqldiag, "r") as diagfile:
                for line in diagfile:
                    if 'sp_configure' in line:
                        next_n_lines = list(islice(diagfile, 71))
                        outputfile.writelines(next_n_lines)
                        break


    print("Got SP_Configure output for " + servername.upper())