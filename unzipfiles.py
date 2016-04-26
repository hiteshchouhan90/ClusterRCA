# Using a function to extract the zip file since we will be calling this multiple times
# Using pyunpack because the input file is .CAB !
# to add to the complexity pyunpack requires either cabextract or 7z to be installed
# Hence I've installed 7z and added "C:\Program Files\7-Zip" to the environment variable
#import pyunpack
import os,sys


def unzipfile(filename,destfolder):
#    Archive(filename).extractall(destfolder)
    try:
        temppath = sys._MEIPASS
    except AttributeError:
        temppath = os.path.abspath(".")

    print("Extracting " + filename)
    os.system(temppath + "\\7z.exe e " + filename + " -o" + destfolder + " -y > nul")
