#Autor: Daniel Gomes Venzi Goncalves    |
#Email: daniel@avantsec.com.br          |
#Propriedade: AvantSec                  |     
#---------------------------------------#

import os
import sys
import json
import time
import random

#---------------------------------------------------------------------------
# Pega o nome (ou endereco) dos hosts que sofrerao o teste de conexao 
# em porta TCP.

def GetHosts():

        if sys.argv[1] == "-n":
                Hosts=[]
                i=3
                while i <= int(sys.argv[2])+2:

                        Hosts.append(sys.argv[i])
                        i += 1

                return Hosts

#---------------------------------------------------------------------------
# Pega as portas que deverao ser testadas nos hosts.

def GetPorts():

        if sys.argv[int(sys.argv[2])+3] == "-p":

		Ports=[]
                PortQnt = int(sys.argv[int(sys.argv[2])+4])
	        i = int(sys.argv[2])+5
		Max = (3+int(sys.argv[2])+PortQnt)+1

                while i <= Max:

                        Ports.append(sys.argv[i])
                        i += 1

                return Ports

#---------------------------------------------------------------------------
# Testa as portas passadas nos hosts passados, e coloca o resultado
# em um array.

def TestTCP(Hosts,Ports):

	FinalResult = []
	i = 0
	while i <= len(Hosts)-1:

		HostResult = []
		j = 0	

		while j <= len(Ports)-1:
			
			ConnectionBool = os.popen("nc -zv {0} {1} &> /dev/null ; echo $?".format(Hosts[i],Ports[j])).read()
			ConnectionBool = ConnectionBool.strip("\n")
			HostResult.append(ConnectionBool)

			j += 1

		FinalResult.append(HostResult)
		i += 1
	
	#print(FinalResult)
	return FinalResult

#---------------------------------------------------------------------------
# Deixa os Hosts, Portas e resultados de conexao em um formato JSON
# afim de facilitar a indexacao

def JSONEncode(Hosts, Ports, Result, time):

	Dicionary = {}
	#i = 0
	#j = 0
	
	#while j <= len(Ports)-1:
	#	Dicionary["Port {0}".format(j+1)] = Ports[j]
	#	j += 1
	#
	#while i <= len(Hosts)-1:
	#	Dicionary["Host {0}".format(i+1)] = Hosts[i]		
	#	i += 1


	i=0
	while i <= len(Hosts)-1:
	
		j=0
		#while j <= len(Ports)-1:
		#	#Dicionary["Host {0} port {1}".format(i,Ports[j])] = Result[i][j]
		#	if Result[i][j] == "0":
		#		Dicionary["Host {0} port {1}".format(i+1,Ports[j])] = "Success"

		#	elif Result [i][j] == "1":
		#		Dicionary["Host {0} port {1}".format(i+1,Ports[j])] = "Failed"

		#	j += 1
		#Dicionary["Host {0}".format(i+1)] = Hosts[i]
		#print("Chegou aqui")	
		while j <= len(Ports)-1:
                       
		       #Dicionary["Port {0}".format(j+1)] = Ports[j] 
                       if Result[i][j] == "0":
				#print("Chegou aqui")
                        	Dicionary["Status"] = "Success"

                       elif Result[i][j] == "1":
                               Dicionary["Status"] = "Failed"

                       j += 1
		i += 1

	GenerateTime = os.popen("date +%s%3N").read()
        GenerateTime = GenerateTime.strip("\n")
        Dicionary["GenerateTime"] = GenerateTime
	Dicionary["Host"] = Hosts
	Dicionary["Port"] = Ports
	Dicionary["Response Time"] = time

        Response = json.dumps(Dicionary, ensure_ascii=False)
        print(Response)

	
Hosts = GetHosts()
Ports = GetPorts()
then = time.time()
Result = TestTCP(Hosts, Ports)
now = time.time()
JSONEncode(Hosts, Ports, Result, now-then)


#print(Hosts)
#print(Ports)
#print(Result)
