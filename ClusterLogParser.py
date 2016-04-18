import glob
from datetime import datetime, timedelta

def ClusterLogParser(rootdirectory,servernames,outputfile,startdate,enddate):
    print("GETTING CLUSTERLOG DETAILS FROM ALL NODES FOR THE MENTIONED TIMEFRAME")
    logFilePath=[]
    sysInfo=[]
    timeZone=""
    offset=0
    count=1
    ignoreList=["Sending request"]
    for servername in servernames:
        if count<=1 or len(logFilePath)==0:
            Clusterlog=glob.glob(rootdirectory + "/" + servername.upper() + "/*cluster.log")[0]
            logFilePath.append(Clusterlog)
            count+=1

    #logFilePath=set(logFilePath)
    for servername in servernames:
        sysInfoFile = glob.glob(rootdirectory + "/" + servername.upper() + "\*System_Information.txt")[0]
        with open(sysInfoFile,"r",encoding="utf-16") as sysInfoFiledata:
            for line in sysInfoFiledata:
                if line.__contains__('Time Zone:'):
                    timeZone=line
                    #print(timeZone)
                    offset=int(timeZone[timeZone.find('-'):int(timeZone.find('-'))+3])

                    tempstartdate=startdate+timedelta(hours=offset)
                    tempenddate=enddate+timedelta(hours=offset)
                    newstartdate=tempstartdate.strftime("%Y/%m/%d-%H:%M:%S")
                    newenddate=tempenddate.strftime("%Y/%m/%d-%H:%M:%S")
                    newstartdate=datetime.strptime(newstartdate,"%Y/%m/%d-%H:%M:%S")
                    newenddate=datetime.strptime(newenddate,"%Y/%m/%d-%H:%M:%S")

                    for path in logFilePath:
                        with open(path,"r",encoding="utf-16") as logs:
                            outputfile.write("\n" + " ANALYZING CLUSTER LOG FOR SERVER" + str(servername) + "\n")
                            #newstartdate=datetime.strptime(str(newstartdate),"%Y/%m/%d-%H:%M:%S")
                            #newenddate=datetime.strptime(str(newstartdate),"%Y/%m/%d-%H:%M:%S")
                            for line in logs:
                                try:
                                    clusterLogTimestamp= datetime.strptime(line[19:38], "%Y/%m/%d-%H:%M:%S")
                                    #print(clusterLogTimestamp)
                                    if (clusterLogTimestamp>newstartdate) and (clusterLogTimestamp<newenddate) and not ([line for x in ignoreList if line.__contains__(x)]):
                                        outputfile.write(line)
                                    else:
                                        pass
                                except:
                                    pass



'''

NOT CONSIDERING DST as we are already taking +-2 in account and there will be a lot of data in cluster Log

                    tzinfo.dst - Gives whether timezone is applicable or not and then we can put if logic around it followed with following :
                        newstartdate = startdate + timedelta(hours=1)
                        newenddate = enddate + timedelta(hours=1)

                    else:
                        newstartdate=newstartdate
                        newenddate=newenddate


Another way is to use pytz with the timezone which takes care of DST as well.
Example to use pytz -- http://pytz.sourceforge.net/
'''