# Using a function to extract the zip file since we will be calling this multiple times
# Using pyunpack because the input file is .CAB !
# to add to the complexity pyunpack requires either cabextract or 7z to be installed
# Hence I've installed 7z and added "C:\Program Files\7-Zip" to the environment variable

from pyunpack import Archive

def unzipfile(filename,destfolder):

    Archive(filename).extractall(destfolder)

# Testing the unzip function
# Giving the destination folder as TempFolder because at this point we don't know to which ServerName the zip file belongs to
# Once extracted we will get the machine name and rename it