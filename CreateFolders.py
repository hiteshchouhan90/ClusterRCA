import os
import glob
from os.path import basename
from unzipfiles import unzipfile

servernames = []

def CreateFirstFolder(inputfilename, filenameonly,rootdirectory):
    """
        Definition::
            This function creates the first folder based on the name of the .cab file provided
            Checks if the directory exists
            If the directory already exists it is removed if not the directory is created
            Then extracting the cab file to this folder

            Later read the *System_Information.txt file name using glob using "_" as the delimiter
            Server name is the 0th element in the list returned
            Finally renaming the original folder to the ServerName obtained
    """

    if not os.path.exists(rootdirectory):
        os.makedirs(rootdirectory + "/" + filenameonly)
    else:
        os.remove(rootdirectory)

    unzipfile(inputfilename, rootdirectory + "/" + filenameonly)

    SysInfoFile = glob.glob(rootdirectory + "/" + filenameonly + "/*System_Information.txt")
    FirstServerName = basename(SysInfoFile[0]).split("_", 1)[0]
    os.rename(rootdirectory + "/" + filenameonly, rootdirectory + "/" + FirstServerName)
    print("Created folder " + rootdirectory + "/" + FirstServerName)

    return FirstServerName

def CreateNextFolders(rootdirectory, FirstServerName, filenameonly):
    """
    Definition::
        Gets the server names based on the naming convention of _cluster.log files found in the FirstServerName
        Check if the folders for the servers exist, if not prompt the user for the subsequent log files

    """
    for clusterlog in glob.glob(rootdirectory + "/" + FirstServerName + "/*_cluster.log"):
        servernames.append(basename(clusterlog).split(("."), 1)[0].upper())

    for servername in servernames:
        if os.path.exists(rootdirectory + "/" + servername.upper()):
            print("Folder " + servername + " exists. Not doing anything here")
        else:
            os.makedirs(rootdirectory + "/" + servername.upper())
            print("Enter the path of the new zip file for server: " + servername.upper())
            inputfilename = input() or "C:\Pradeep\Data\SDP2.cab"
            unzipfile(inputfilename, rootdirectory + "/" + servername.upper())
            print("Created folder " + rootdirectory +  "/" + servername.upper())

    return servernames