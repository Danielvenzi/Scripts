#                                                 |
#Autor: Daniel Gomes Venzi Goncalves              |
#Email: daniel@avantsec.com.br                    |
#Propriedade: AvatSec                             |
#-------------------------------------------------#

import os 
import sys
import json

def GetHosts():

        if sys.argv[1] == "-n":
                Hosts=[]
                i=3
                while i <= int(sys.argv[2])+2:
                        #print(sys.argv[i])
                        Hosts.append(sys.argv[i])
                        i += 1
                return Hosts


def PingErr():

	ping = os.system("ping -c 1 {0} > res".format(sys.argv[1]))
	#os.system("cat ./res")
	Received = str(os.popen("cat ./res | grep transmitted |grep -Po 'transmitted, \K\d{1}'").read())
	Received = Received.strip("\n")
	return Received


if sys.argv[1] == "":
	print("Wrong usage of command.") 

elif sys.argv[1] != "":

	#Hosts = GetHosts()
	#print(Hosts)
	Bool = PingErr()		

	if Bool == "0":

		PingDict = {}
		GenerateTime = os.popen("date +%s%3N").read()
		GenerateTime = GenerateTime.strip("\n")
		PingDict["GenerateTime"] = GenerateTime
		PingDict["Host IP"] = sys.argv[1]
		PingDict["Ping Status"] = "Failed"
		Response = json.dumps(PingDict, ensure_ascii=False)
		print(Response)

	elif Bool == "1":
	
		#Usa expressao grep com expressao regular para pegar os valores de TTL e Time da resposta do ping

		PingTTL = str(os.popen("cat ./res | grep '64 bytes' | grep -Po 'ttl=\K\d{1,}'").read())
		PingTTL = PingTTL.strip("\n")
		PingTime = str(os.popen("cat ./res | grep '64 bytes' |grep -Po 'time=\K\d{1,}.\d{1,}'").read())
		PingTime = PingTime.strip("\n")

		#Cria um dicionario com os valores TTL e TIME para depois retornar um JSON.

		PingDict = {}
		GenerateTime = os.popen("date +%s%3N").read()
		GenerateTime = GenerateTime.strip("\n")
		PingDict["GenerateTime"] = GenerateTime
		PingDict["Ping Status"] = "Success"
		PingDict["Host IP"] = sys.argv[1]
		PingDict["Ping TTL"] = PingTTL
		PingDict["Ping Time"] = PingTime
	        
		os.system("rm -f /root/AUTO_SCRIPT/Scripts/avantdata_scripts/avantzabbix/Ping/res")

		Response = json.dumps(PingDict, ensure_ascii=False)	
		print(Response) 		
