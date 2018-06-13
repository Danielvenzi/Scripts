import os
import sys
import json


def HostsGet():

	if sys.argv[1] == "-n":
		Hosts=[]		
		i=3
		while i <= int(sys.argv[2])+2:
			#print(sys.argv[i])		
			Hosts.append(sys.argv[i])
			i += 1
		return Hosts

def ServerGet():

	if sys.argv[1] == "-n":
		
		if sys.argv[int(sys.argv[2])+3] == "-s":
			Server = sys.argv[int(sys.argv[2])+4]	
			#print(Server)

			return Server

#print(len(HostsCheck()))
#ServerGet()

#print(len(sys.argv))
#print(4+int(sys.argv[2])+1)

#Hosts = HostsGet()
#ServerName = ServerGet()
#Results = []
#ServerStat = []

if 4+int(sys.argv[2])+1 == len(sys.argv):
	
	Hosts = HostsGet()
	ServerName = ServerGet()
	Results = []
	ServerStat = []



	for host in Hosts:
		Result = os.popen("host {0} {1} | grep '{2} has address' | grep -Po '.*address \K\d+.\d+.\d+.\d+'".format(host,ServerName,host)).read()
		
		if Result == "":
			ServerStat.append("Failed")			

		elif Result != "":
			Result = Result.strip("\n")
			#print(Result)
			Results.append(Result)
			ServerStat.append("Success")

	i=0		
	while i <= len(Hosts)-1:
		print(Results[i])
		print(ServerStat[i])	
		i += 1
			 		
elif 4+int(sys.argv[2])+1 != len(sys.argv):
	
	Hosts = HostsGet()
	Results = []
	ServerStat = []	

	for host in Hosts:
                Result = os.popen("host {0} | grep '{1} has address' | grep -Po '.*address \K\d+.\d+.\d+.\d+'".format(host,host)).read()

                if Result == "":
                        ServerStat.append("Failed")

                elif Result != "":
                        Result = Result.strip("\n")
                        #print(Result)
                        Results.append(Result)
                        ServerStat.append("Success")

        i=0
        while i <= len(Hosts)-1:
                print(Results[i])
                print(ServerStat[i])
                i += 1
