from datetime import datetime, timedelta
import glob
import fnmatch
import os
def ErrorLogParser(startdate,enddate,rootdirectory, servernames, instancenames,outputfile):
    baseErrorLogName = ""
    #startdate = datetime.strptime(startdate,"%Y/%m/%d %H:%M")
    startdate=startdate.strftime("%Y-%m-%d %H:%M:%S")
    startdate = datetime.strptime(startdate,"%Y-%m-%d %H:%M:%S")
    ignoreList=["DbMgrPartnerCommitPolicy","Log was backed up"]

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
            flag=1
            #print("value for file number is " + str(FileNumber))
            outputfile.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
            outputfile.write("GETTING ERRORLOG DETAILS for " + LogFileName +"\n")
            outputfile.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
            with open(LogFileName, "r", encoding="utf-16") as errorlog:
                duplicateMessage=""
                duplicateMessageCount=1
                tempMessage=""
                InnerMessages=[]
                InnerFlag=0
                for line in errorlog:
                    try:
                        errorlogtimestamp = datetime.strptime(line[0:19], "%Y-%m-%d %H:%M:%S")
                        if (errorlogtimestamp >= startdate) and (errorlogtimestamp <= enddate):
                            #duplicateMessage=line
                            #outputfile.write(line)
                            flag=1
                            try:
                                onlyMessageTemp = line[35:]
                                ErrorValue=""
                                if "Error:" in onlyMessageTemp:
                                    #outputfile.write("skipping as this is error line")
                                    ErrorValue=onlyMessageTemp

                                elif ([onlyMessageTemp for x in ignoreList if onlyMessageTemp.__contains__(x)]):
                                    pass

                                else:
                                    onlyMessage=onlyMessageTemp
                                    #outputfile.write("\n-------------------------------------------------------------------- \n")
                                    #outputfile.write("the only message is " + onlyMessage)
                                    #outputfile.write("temp message is " + tempMessage)
                                    #outputfile.write("duplicate message count is " + str(duplicateMessageCount))
                                    #outputfile.write("\n-------------------------------------------------------------------- \n")
                                    if onlyMessage==tempMessage:
                                        duplicateMessage=line
                                        duplicateMessageCount+=1
                                        #outputfile.write("\n------------------inside onlyMessage==tempMessage------------------ \n")
                                        #outputfile.write("the message is " + onlyMessage)
                                        #outputfile.write("temp message is " + tempMessage)
                                        #outputfile.write("duplicate message count is " + str(duplicateMessageCount))
                                        #outputfile.write("\n-------------------------------------------------------------------- \n")

                                    elif (onlyMessage!=tempMessage) and (duplicateMessageCount>1):
                                        outputfile.write("\n")
                                        outputfile.write("error value is"+ str(ErrorValue))
                                        outputfile.write(duplicateMessage)
                                        outputfile.write("\n Above message appeared " + str(duplicateMessageCount) +" times\n")
                                        outputfile.write("\n------------------------------------------------------------\n")
                                        tempMessage = onlyMessage
                                        #outputfile.write("in Elif")
                                        duplicateMessageCount=0

                                    else:
                                        tempMessage=onlyMessage
                                        outputfile.write(line)
                            except:
                                pass

                        if (errorlogtimestamp<startdate):
                            flag=0
                    except:
                        pass
                if flag==0:
                    outputfile.write("Timestamp in ERRORLOG is smaller then the start date hence skipping rest of the log files." + str(errorlogtimestamp))
                    break
            LogFileName=LogFileNameIterator+str(FileNumber)