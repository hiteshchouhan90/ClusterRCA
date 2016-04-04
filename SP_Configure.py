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
        outputfile.write("~" * 15 + "\n" + "SQL Server Configuration Details: " + servername + "\n" + "~" * 15 + "\n" * 2)
        sqldiag = glob.glob(rootdirectory + "/" + servername.upper() + "\*sp_sqldiag_Shutdown")
        with open(sqldiag, "r") as diagfile:
            for line in diagfile:
                if line == "-> sp_configure":
                    outputfile.writelines (''.join(islice(diagfile,71)))
                    break


    print("Got SP_Configure output for " + servername.upper())