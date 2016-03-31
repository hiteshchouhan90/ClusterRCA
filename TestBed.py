import sys
import os
from zipfile import stringEndArchive64Locator

string = ["CW750SHPTPS01N2_MSSQLSERVER_1033_ERRORLOG", "CW750SHPTPS01N2_Instance1_1033_ERRORLOG"]
string = set(string)
instancename =[]
for item in string:
    i = str(item).split("_")
    instancename.append(i[1])
print(instancename)
# string = string.replace("CW750SHPTPS01N2_","")
