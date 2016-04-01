import sys
import os
from zipfile import stringEndArchive64Locator

string = [["CW750SHPTPS01N2","MSSQLSERVER","1033","ERRORLOG"], ["CW750SHPTPS01N2","Instance1","1433","ERRORLOG"]]
lookfor =["1433","1033","Instance"]
for items in string:
    if any(item in (items[2],items[1]) for item in lookfor):
        print(items )
