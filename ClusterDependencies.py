import sys
import os
import glob

def GetClusterDependencies(rootdirectory, servernames,outputfile):

    """
    This module fetches the dependencies of the Cluster resources from the "_DependencyReport.mht" file
    The dependencies are stored in this file under the tag --> <div class=3D\"info\">
    The code reads the MHTfile to find if it has <div class=3D\"info\"> or not
    If it does then select the text between the tag and </div>

    Also ignoring "img src" as we are not interested in the dependency diagram instead just the text
    Ignoring "has not required dependencies" as expected, to keep the output clean

    :param rootdirectory: We are passing the rootdirectory from the variable in main.py
    :param servernames: We are passing the ServerNames list from the variable in main.py
    :param outputfile:  We are passing the Output file from the variable in main.py
    :return:

    """
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
    print("Got the Cluster resources dependency report")