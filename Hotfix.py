import os
import sys
import glob
import re

def GetHotFix(rootdirectory, servernames,outputfile):

    """
    This will fetch the hotfixes(KB) installed on all the servers
    For the first time in the project we're using regular expressions i.e. to look for the word KB
    The values for each server is stored in KBListname. Once all values are stored, inserting the ServerName as the 0th element in the list
    Hotfixes for all the servers are stored in FinalList as list of list (by appending KBListName)
    Finally loop through the FinalList and get the missing hotfixes by converting the list into a set, substracting it from the set of previous list
    
    """

    FinalList = []
    for servername in servernames:
        hotfixfile = glob.glob(rootdirectory + "/" + servername.upper() + "/*_Hotfixes.TXT")[0]



        KBListNames = "kb"+servername.upper()
#        KBListNames.append(KBListName)
        KBListName = []

        with open(hotfixfile, "r", encoding="utf-8") as Hotfix:
            for line in Hotfix:
                #columns = line.split("  ")
                #KBListName.append(columns[4:5])
            #print(KBListName[3:])
                column = str(line.split(' '))
                m = str(re.findall(r'\bKB.*\b', column))
                string = m.split(',')
                KBArticles = re.sub('["\'\[\]]', '', string[0])
                KBListName.append(KBArticles)
            KBListName[0]=servername
            FinalList.append(KBListName)
#            print(KBListName)
#            print(FinalList[:100])

    #Comparing the dynamically created lists
    i=0
    while i<len(FinalList):
        outputfile.write("~" * 20 +"\n")
        outputfile.write("Hotfixes missing on Server: " + FinalList[i][0])
        outputfile.write("\n" + "~" * 20 +"\n")
        outputfile.write(str(set(FinalList[i][1:]) - set(FinalList[i - 1][1:])))
        outputfile.write("\n"*2)
        i=i+1

    print("Got hotfix information")
    #
    #
