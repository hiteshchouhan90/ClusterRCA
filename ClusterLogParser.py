import glob
from datetime import datetime, timedelta

def GetClusterLogs(rootdirectory,servernames,outputfile,startdate,enddate):

    """
    The parameters are self-explanatory and they are passed from variables in main.py
    Cluster log's entries are saved in UTC timezone

    Since the servers are in different timezone most of the times, we need to take into account the Day Light Saving also
    Throughout the application we've maintained the standard to fetch records +2/-2 hours from the user input date/time
    Since DST will be +1/-1 hours, not taking the DST into account here as our logic has already covered the extra 2 hours

    In case we change our minds in future, the following example will be a good start to include DST

                        tzinfo.dst - Gives whether timezone is applicable or not and then we can put if logic around it followed with following :
                        newstartdate = startdate + timedelta(hours=1)
                        newenddate = enddate + timedelta(hours=1)

                    else:
                        newstartdate=newstartdate
                        newenddate=newenddate


    Another way is to use pytz with the timezone which takes care of DST as well.
    Example to use pytz -- http://pytz.sourceforge.net/



    """

    print("Getting data from clusterlog for mentioned timeframe")
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

        """
        Getting the time zone information from the one of the lines in System_Information.txt

       """
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

    print("Got clusterlog data")