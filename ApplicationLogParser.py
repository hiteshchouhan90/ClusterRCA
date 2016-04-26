import re
import traceback
import glob
import csv
from datetime import datetime

def GetApplicationLog(rootdirectory, servernames,outputfile,startdate, enddate):
    print("Getting Application log data for the given timeframe")
    ApplogIgnoreList = []

# First converting the date time to match the System Event Log format i.e. 01/26/2016 05:14:34 AM
    startdate = startdate.strftime("%m/%d/%Y %I:%M:%S %p")
    enddate = enddate.strftime("%m/%d/%Y %I:%M:%S %p")

    convertedStartDate = datetime.strptime(startdate, "%m/%d/%Y %I:%M:%S %p")
    convertedEndDate = datetime.strptime(enddate, "%m/%d/%Y %I:%M:%S %p")
    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "Application Event Log of " + servername + "\n" + "~" * 20 + "\n" * 2)
        ApplicationEventLog = glob.glob(rootdirectory + "/" + servername.upper() + "\*_evt_Application.csv")[0]

        with open(ApplicationEventLog, "r", encoding="utf-8") as AppEvtLog:
            duplicateMessage = ""
            duplicateMessageCount = 1
            tempMessage = ""
            AppCSV = csv.reader(AppEvtLog, delimiter=',')

            for line in AppCSV:
                #print("in line")
                try:
                    logtimestamp=datetime.strptime(line[0] + " " + line[1], "%m/%d/%Y %I:%M:%S %p")
                    #outputfile.write("\n"+"log time stamp" + str(logtimestamp))
                    #print(type(logtimestamp),type(convertedEndDate),type(convertedStartDate))
                    #outputfile.write("\n"+"start date" + str(convertedStartDate))
                    #outputfile.write("\n"+"end date " + str(convertedEndDate)+"\n")

                    if(logtimestamp>= convertedStartDate) and (logtimestamp <= convertedEndDate):
                        onlyMessageTemp = line[8]
                        ErrorValue = ""
                        #outputfile.write("within time range")

                        if "Error:" in onlyMessageTemp:
                            ErrorValue = onlyMessageTemp
                            outputfile.write("line contains word Error")

                        elif ([onlyMessageTemp for x in ApplogIgnoreList if onlyMessageTemp.__contains__(x)]):
                            #outputfile.write("in elif")
                            pass

                        else:
                            onlyMessage = onlyMessageTemp
                            #outputfile.write("temp messsage is " +tempMessage+"\n")
                            #outputfile.write("only message is "+onlyMessage+"\n")

                            if onlyMessage == tempMessage:
                                #outputfile.write("duplicate message count" +str(duplicateMessageCount))
                                duplicateMessage = line
                                duplicateMessageCount += 1

                            elif (onlyMessage != tempMessage) and (duplicateMessageCount > 1):
                                duplicateMessage=str(duplicateMessage)
                                #outputfile.write("in duplicate code")
                                printmessage=re.sub(",|'|\[|\]" , "" ,duplicateMessage)
                                outputfile.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
                                outputfile.write(printmessage)
                                outputfile.write("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                                outputfile.write("\n Above message appeared " + str(duplicateMessageCount) + " times\n")
                                tempMessage = onlyMessage
                                duplicateMessageCount = 0

                            else:
                                tempMessage = onlyMessage
                                printmessage = re.sub(",|'|\[|\]", "", str(line))
                                outputfile.write(printmessage)
                                outputfile.write("\n")
                except:
                    #print(traceback.format_exc()) --> kept for error reporting if we include at some point
                    pass

    print("Got Application event logs")
#print(traceback.format_exc())


