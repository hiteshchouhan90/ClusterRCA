import sys
import os
import glob

def GetClusterDependencies(rootdirectory, servernames,outputfile):
    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "Cluster dependency report for  " + servername + "\n" + "~" * 20 + "\n" * 2)
        DepFile = glob.glob(rootdirectory + "/" + servername.upper() + "\*_DependencyReport.mht")[0]
        with open(DepFile, "r") as MHTFile:
            for line in MHTFile:
                if ("<div class=3D\"info\">" in line) and ("img src=" not in line) and ("has no required dependencies." not in line):
                    newline = line.replace("<div class=3D\"info\">", "")
                    newline = newline.replace("</div>", "")
                    outputfile.write(newline)
        outputfile.write("\n" * 2)

    outputfile.write("\n")
    print("Got Storage/Network drives")