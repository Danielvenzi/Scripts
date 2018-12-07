#!/usr/bin/python


import sys
import os

COMMAND_LINE=sys.argv[1]

#print(COMMAND_LINE)

Total = os.popen("echo {0} | cut -d':' -f4".format(COMMAND_LINE)).read()
Used = os.popen("echo {0} | cut -d':' -f5".format(COMMAND_LINE)).read()
Percent = float(Used)/float(Total)
Percent = round(Percent,2)
#print(Total)
#print(Used)

print(COMMAND_LINE+str(Percent))
