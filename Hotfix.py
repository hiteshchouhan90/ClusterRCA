import os
import sys
import glob

def GetHotFix(rootdirectory, servernames,outputfile):
    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "Filter Drivers loaded on " + servername + "\n" + "~" * 20 + "\n" * 2)
        hotfixfile = glob.glob(rootdirectory + "/" + servername.upper() + "/*_Hotfixes.TXT")[0]
        KBListName = "kb"+servername.upper()
        print(KBListName)
        KBListName =[]
        print(KBListName)
        with open(hotfixfile, "r", encoding="utf-8") as Hotfix:
            for line in Hotfix:
                columns = line.split("  ")
                KBListName.append(columns[4:5])
            print(KBListName[3:])

    # Comparing the dynamically created lists




