import sys, glob, os
from itertools import islice
from operator import itemgetter

with open("C:\Python35\Scripts\dist\SDP\COCTXSQLPRD01\CTXSQLPRD_MSSQLSERVER_1033_sp_sqldiag_Shutdown.OUT", "r") as diagfile:
    start = 0
    linecount=0
    waitstatslist=[]
    for line in diagfile:
        if 'sys.dm_os_wait_stats' in line:
            start =1
            linecount=1
#            next_n_lines = list(islice(diagfile, 71))
        if 'sys.dm_os_waiting_tasks' in line:
            break


        if start==1:
            if linecount>3:
                if len(line)>3 and "FULLTEXT GATHERER" not in line:
                    waitstatslist.append(line.split())
            linecount+=1

    linecount=0
    waitstatslist.sort(key= lambda waitstat: int(waitstat[2]), reverse=True)
    for item in waitstatslist:
        if linecount<6:
            print(item[0] + "\t"*4 + item[2])
        linecount+=1

