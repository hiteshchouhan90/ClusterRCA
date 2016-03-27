# Using a function to extract the zip file since we will be calling this multiple times
# Using pyunpack because the input file is .CAB !
# to add to the complexity pyunpack requires either cabextract or 7z to be installed
# Hence I've installed 7z and added "C:\Program Files\7-Zip" to the environment variable

import zipfile
from datetime import datetime

# Get location of a SDP file
sdplocation=input("Please provide zipped SDP file: ")

new_path = '%s_%s' % (datetime.now().strftime(FORMAT), path)

# Extract all the files from the compressed archive
with zipfile.ZipFile(sdplocation, "r") as z:
    z.extractall("C:\\test\\")

# Testing the unzip function
# Giving the destination folder as TempFolder because at this point we don't know to which ServerName the zip file belongs to
# Once extracted we will get the machine name and rename it