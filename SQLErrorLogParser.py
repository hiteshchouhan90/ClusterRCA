from datetime import datetime, timedelta
import glob
import fnmatch
import os
def ErrorLogParser(startdate,enddate,rootdirectory, servernames, instancenames,outputfile):
    baseErrorLogName = ""
    #startdate = datetime.strptime(startdate,"%Y/%m/%d %H:%M")
    startdate=startdate.strftime("%Y-%m-%d %H:%M:%S")
    startdate = datetime.strptime(startdate,"%Y-%m-%d %H:%M:%S")


    enddate=enddate.strftime("%Y-%m-%d %H:%M:%S")
    enddate = datetime.strptime(enddate,"%Y-%m-%d %H:%M:%S")

    #print(rootdirectory)
    for serverName in servernames:
        totalLogFiles = []
        for instancename in instancenames:
            for file in os.listdir(rootdirectory + '/' + serverName.upper() ):
                if serverName in file and instancename in file and "ERRORLOG" in file:
                    baseErrorLogName=file
                    totalLogFiles.append(file)
        TempErrorLogName=baseErrorLogName.split('.')
        baseErrorLogName=TempErrorLogName[0]

        LogFileName = rootdirectory + "/" + serverName.upper() + "/" + baseErrorLogName
        LogFileNameIterator=LogFileName+"."
        #print("server name is " + serverName)
        #print("value of totalLogFiles is " + str(len(totalLogFiles)))
        for FileNumber in range(1,len(totalLogFiles)):
            flag=0
            #print("value for file number is " + str(FileNumber))
            outputfile.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
            outputfile.write("GETTING ERRORLOG DETAILS for " + LogFileName +"\n")
            outputfile.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
            with open(LogFileName, "r", encoding="utf-16") as errorlog:
                duplicateMessage=[]
                duplicateMessageCount=1
                #print("ERROR LOG Module starting")
                #outputfile.write("--------------------Starting Logfile ----------------------" + LogFileName + "\n" )
                for line in errorlog:
                    try:
                        errorlogtimestamp = datetime.strptime(line[0:19], "%Y-%m-%d %H:%M:%S")
                        if (errorlogtimestamp >= startdate) and (errorlogtimestamp <= enddate):
                            duplicateMessage.append(line)
                            outputfile.write(line)
                            flag=1

                        if (errorlogtimestamp<startdate):
                            flag=0
                    except:
                        pass
                if flag==0:
                    outputfile.write("Timestamp in errorlog is smaller then the start date hence skipping rest of the log files.")
                    break
            LogFileName=LogFileNameIterator+str(FileNumber)