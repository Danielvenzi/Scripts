#----------------------------------------# 
# Autor: Daniel Gomez Venzi Gonçalves    |
# E-mail: daniel@avantsec.com.br         |
# Empresa: AvantSec                      |
#----------------------------------------#


import os
import sys
import subprocess

def Action (bole,text):
    if bole == 0:
        ports.append(text)

port = open("port.info","r")
ports = []

for line in port:

    line = line.strip('\n')
    results = str(os.popen("echo {0} | grep -Po ':\K\d+'".format(line)).read())
    results = results.strip('\n')
    i = 0
    BOOLE = 0

    if len(ports) == 0 :
        ports.append(results)
        BOOLE = 1

    elif len(ports) != 0:
     
        while i < (len(ports)):
            if results == ports[i]:
                 BOOLE=1
                 break
            i += 1

    Action(BOOLE,results)

os.system("rm -f ./port.info")

i=0
result = ""
while i < (len(ports)):
    if i == (len(ports)-1):
        result=result+ports[i]
        break
    elif i != (len(ports)-1):
        result = result+ports[i]+","
    i += 1

print(result)    
