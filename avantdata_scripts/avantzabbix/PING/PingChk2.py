import sys
import json
import os


#-------------------------------------------------------------
# Pega os hosts passados como argumento.

def GetHosts():

        if sys.argv[1] == "-n":
                Hosts=[]
                i=3
                while i <= int(sys.argv[2])+2:
                        #print(sys.argv[i])
                        Hosts.append(sys.argv[i])
                        i += 1
                return Hosts

#-------------------------------------------------------------
# Ping os hosts passados.

def PingHosts():




print(GetHosts())
