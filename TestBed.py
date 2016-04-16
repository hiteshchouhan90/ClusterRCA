import os
import subprocess


cmd=r"7z e C:\Pradeep\Data\SDP.cab -oC:\Pradeep\Data\SDP -y"
print(cmd)
os.system(cmd)