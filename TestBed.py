import sys
import os
from zipfile import stringEndArchive64Locator

with open("C:\Pradeep\Data\samplemhtfile.mht", "r") as MHTFile:
    for line in MHTFile:
        start = 0
        if ("<div class=3D\"info\">" in line) and ("img src=" not in line) and ("has no required dependencies." not in line):
                newline = line.replace("<div class=3D\"info\">","")
                newline = newline.replace("</div>", "'")
                print(newline)
