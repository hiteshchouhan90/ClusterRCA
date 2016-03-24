# Using a function to extract the zip file since we will be calling this multiple times

import zipfile
def unzipfile(filename,destfolder):
    filetoextract = zipfile.ZipFile(filename, 'r')
    destdir = destfolder
    filetoextract.extractall(destdir)
    filetoextract.close()

