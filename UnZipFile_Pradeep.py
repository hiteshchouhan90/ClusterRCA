import zipfile

filetoextract = zipfile.ZipFile("Data\\Dummy\\Test.zip", 'r')
destdir = "Data/Dummy/Extract"
filetoextract.extractall(destdir)
filetoextract.close()