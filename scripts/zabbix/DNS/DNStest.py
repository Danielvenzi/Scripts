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

	#print("With server")	
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

			 		
elif 4+int(sys.argv[2])+1 != len(sys.argv):
	
	#print("With no server")
	Hosts = HostsGet()
	ServerName = os.popen("nmcli | grep servers | grep -Po '\d+.\d+.\d+.\d+'").read()
	ServerName = ServerName.strip("\n")
	#print(ServerName)
	Results = []
	ServerStat = []	
	HostFinal = []

	for host in Hosts:
		Lines = os.popen("host {0} | grep '{1} has address' | wc -l".format(host,host)).read()
		Lines = Lines.strip("\n")
		Lines = int(Lines)
		#print(Lines)
		
		if Lines == 1:
                	Result = os.popen("host {0} | grep '{1} has address' | grep -Po '.*address \K\d+.\d+.\d+.\d+'".format(host,host)).read()
	
	                if Result == "":
	                        ServerStat.append("Failed")
	
	                elif Result != "":
	                        Result = Result.strip("\n")
	                        #print(Result)
				HostFinal.append(host)
	                        Results.append(Result)
	                        ServerStat.append("Success")

		elif Lines != 1 and Lines != 0:
			os.system("host {0} | grep '{1} has address' > addr".format(host,host))
			#print(Addresses)
			Addresses = open("addr","r")			
			Addr = open("lala","w")

			for line in Addresses:
				
				#print(line)
				Addr = open("lala","w")
				Addr.write(line)
				Result = os.popen("cat lala | grep -Po '.*address \K\d+.\d+.\d+.\d+'".format(line)).read()
				Result = Result.strip("\n")	
				print(Result)
				
				if Result == "":
					HostFinal.append(host)
					ServerStat.append("Failed")

				elif Result != "":
					#print("Chegou aqui")
					HostFinal.append(host)
					Results.append(Result)
					ServerStat.append("Success")		
				
				os.system("rm -f ./lala")
		
		elif Lines == 0:
			ServerStat.append("Failed")
				
	
LogInput = {}
i=0
while i <= len(Hosts)-1:

	if ServerStat[i] == "Success":
		LogInput["Host "+str(i)] = HostFinal[i]
		LogInput["Host "+str(i)+" IP Address"] = Results[i]
		LogInput["DNS Server"] = ServerName
		LogInput["Status "+str(i)] = "Success"

	elif ServerStat[i] == "Failed":
		LogInput["Host "+str(i)] = HostFinal[i]
		LogInput["DNS Server"] = ServerName
		LogInput["Status "+str(i)] = "Failed"
		
	i += 1

GenerateTime = os.popen("date +%s%3N").read()
GenerateTime = GenerateTime.strip("\n")
LogInput["GenerateTime"] = GenerateTime

Response = json.dumps(LogInput, ensure_ascii=False)
print(Response)
