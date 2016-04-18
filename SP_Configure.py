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
from operator import itemgetter

def GetSPConfigure(rootdirectory, servernames,outputfile):
    for servername in servernames:


        if len(glob.glob(rootdirectory + "/" + servername.upper() + "\*sp_sqldiag_Shutdown.OUT"))>0:
            sqldiag = glob.glob(rootdirectory + "/" + servername.upper() + "\*sp_sqldiag_Shutdown.OUT")[0]
            outputfile.write("~" * 30 + "\n" + "SQL Server Configuration Details: " + servername + "\n" + "~" * 30 + "\n" * 2)

            with open(sqldiag, "r") as diagfile:
                for line in diagfile:
                    if '-> sp_configure' in line:
                        next_n_lines = list(islice(diagfile, 71))
                        outputfile.writelines(next_n_lines)
                        break

                outputfile.write("\n" *2+"~" * 30 + "\n" + "Loaded Modules: " + servername + "\n" + "~" * 30 + "\n" * 2)


                print('Trying to search wait stats')
                cols={}
                headers={}
                delim=' '
                lnum=0
                found=0
                for line in diagfile:
                    if '-> sys.dm_os_wait_stats' in line:
                        found=1
                        print('*********************found wait stats***********************')
                        line=next(diagfile)
                        headers=line.split(None)
                        i = 0
                        # print('printing headers from FOR loop')
                        # print (headers)
                        for heading in headers:
                            heading = heading.strip()
                            cols[heading] = []
                            headers[i] = heading
                            i+=1
                            #print(heading)

                        line=next(diagfile,2)

                    elif ('->' in line or '--' in line) and found==1:
                        print('hitting break')
                        break

                    elif found==1:
#                        print(heading)
#                         print('Printing headers')
#                         print(headers)
#                         print('print columns')
#                         print(cols)
                        if 'GATHERER' in line:
                            continue

                        cells=line.split(None)
                        i=0
                        for cell in cells:
                            cell=cell.strip()
                            # print (cell)
                            # print (i)
                            cols[headers[i]] += [cell]
                            i += 1

                    else:
                        continue



                start=0
                for line in diagfile:
                    if '-> sys.dm_os_loaded_modules' in line:
                        start=1
                        for line2 in diagfile:
                            if 'Microsoft' not in line2 and 'os_nodes'not in line2:
                                outputfile.write(line2)
                            elif '->' in line2:
                                break
                    elif start == 1:
                        break
    #print (cols)
    sorted_cols=sorted(cols,key=itemgetter(3),reverse=True)
    cols['waiting_tasks_count']
    #outputfile.write(cols)
#    print (sorted(cols['wait_time_ms],key=itemgetter(2)))
    print("Got SP_Configure output for " + servername.upper())