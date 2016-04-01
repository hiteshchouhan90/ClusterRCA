import sys
import os
import glob
from os.path import basename
import csv
from datetime import datetime

def GetStorageNetworkDrivers(rootdirectory, servernames,outputfile):
    DriverList =["ATAPI Driver Extension","SCSI Port Driver", "Microsoft Storage Port Driver", "Ethernet"]
    for servername in servernames:
        outputfile.write("~" * 20 + "\n" + "Storage/Network drivers of " + servername + "\n" + "~" * 20 + "\n" * 2)
        DriverFile = glob.glob(rootdirectory + "/" + servername.upper() + "\*_sym_Drivers.CSV")[0]
        with open(DriverFile, "r") as Driver:
            DriverCSV = csv.reader(Driver, delimiter=',')
            start = 0
            for line in DriverCSV:
                if len(line)>=4:
                    if any(item in line[16] for item in DriverList) :
                        outputfile.write(line[3] + "\t" + line[14] + "\t" + line[7] + "\t" + line[15] + "\t" + line[16] + "\n")
        outputfile.write("\n" * 2)

    outputfile.write("\n")
    print("Got Storage/Network drives")