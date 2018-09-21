#AUTOR: Daniel Gomes Venzi       |
#EMAIL: daniel@avantsec.com.br   |
#PROPRIEDADE: AvantSec           |
#--------------------------------#

import os
import sys
import json
import time
import random

#---------------------------------------------------------------------------
# Pega o nome dos hosts que devem ser resolvidos como teste.

def GetHosts():

	if sys.argv[1] == "-n":
		Hosts=[]		
		i=3
		while i <= int(sys.argv[2])+2:
			#print(sys.argv[i])		
			Hosts.append(sys.argv[i])
			i += 1
		return Hosts

#---------------------------------------------------------------------------
# Pega o servidor DNS que sera utilizado para se resolver os hosts.

def GetPassedServer():

	if sys.argv[1] == "-n":
		
		if sys.argv[int(sys.argv[2])+3] == "-s":
			Server = sys.argv[int(sys.argv[2])+4]	
			#print(Server)

			return Server

#---------------------------------------------------------------------------
# Pega  o nome do servidor DNS padrao o qual sera utilizado para resolver
# o endereco dos hosts passados para o script.

def GetDefaultServer():

	ServerName = os.popen("nmcli | grep servers | grep -Po '\d+.\d+.\d+.\d+' | sed -n 1p").read()
        ServerName = ServerName.strip("\n")

	return ServerName

#---------------------------------------------------------------------------
# Verifica se utilizara o servidor DNS padrao ou um servidor DNS terceiro,
# tal verificacao e baseada na quantidade de parametros passados.

def IfServerIsDefault():

	if 4+int(sys.argv[2])+1 == len(sys.argv):
		Bool = 1

	elif 4+int(sys.argv[2])+1 != len(sys.argv):
		Bool = 0

	return Bool

#---------------------------------------------------------------------------
# Pega o endereco de um host no caso de ele ter somente um endereco,
# varia no funcionamento no caso de ser utilizado um servidor passado
# ou se utilizar o servidor padrao.

def ResolveOne(Host,Bool):

	Final = []
        Addr = []
        ServerStat = []

        if Bool == 1:

                Result = os.popen("host {0} {1} | grep '{2} has address' | grep -Po '.*address \K\d+.\d+.\d+.\d+'".format( Host, GetPassedServer(), Host)).read()

                if Result == "":
                        Addr.append("N/A")
                        ServerStat.append("Failed")

                elif Result != "":
                        Result = Result.strip("\n")
                        Addr.append(Result)
                        ServerStat.append("Success")

		HostName = []
		HostName.append(Host)

		ServerName = []			
		Server = GetPassedServer()
		ServerName.append(Server)

		Final.append(HostName)
        	Final.append(ServerStat)
        	Final.append(Addr)
		Final.append(ServerName)
		
	
	        return Final
	
	elif Bool == 0:

		Result = os.popen("host {0} | grep '{1} has address' | grep -Po '.*address \K\d+.\d+.\d+.\d+'".format(Host,Host)).read()

		if Result == "":
                        Addr.append("N/A")
                        ServerStat.append("Failed")

                elif Result != "":
                        Result = Result.strip("\n")
                        Addr.append(Result)
                        ServerStat.append("Success")

		HostName = []
                HostName.append(Host)

		ServerName = []
		Server = GetDefaultServer()
		ServerName.append(Server)

		Final.append(HostName)
                Final.append(ServerStat)
                Final.append(Addr)
		Final.append(ServerName)


                return Final

#---------------------------------------------------------------------------
# Pega os enderecos de um host no caso de ele ter mais de um endereco.

def ResolveSeveral(Host,Bool):

	Main = []
	Addr = []
	HostName = []
	ServerStat = []
	Server = []
	Result = []

	if Bool == 1:
		Addresses = open("/usr/local/bin/addr","w")
		Addrs=os.popen("host {0} {1} | grep '{2} has address'".format(Host,GetPassedServer(),Host)).read()
		Addresses.write(Addrs)
		Addresses.close()
		Addresses = open("/usr/local/bin/addr","r")
		
		for line in Addresses:
			line = line.strip("\n")
			Addre = os.popen("echo {0} | grep '{1} has address' | grep -Po '\K\d+.\d+.\d+.\d+'".format(line,Host)).read()
			Addre = Addre.strip("\n")
			Addr.append(Addre)
							
		ServerStat.append("Success")
		HostName.append(Host)
		Server.append(GetPassedServer())

		Result.append(HostName)
		Result.append(ServerStat)
		Result.append(Addr)
		Result.append(Server)
		
		#Main.append(Result)

		
		
		#return Main
		return Result

	elif Bool == 0:	
		Addresses = open("/usr/local/bin/addr","w")
		Addrs=os.popen("host {0} | grep '{1} has address'".format(Host, Host)).read()
		Addresses.write(Addrs)
		Addresses.close()
		Addresses = open("/usr/local/bin/addr","r")

		for line in Addresses:
			line = line.strip("\n")
			Addre = os.popen("echo {0} | grep '{1} has address' | grep -Po '\K\d+.\d+.\d+.\d+'".format(line,Host)).read()
			Addre = Addre.strip("\n")
			Addr.append(Addre)

                ServerStat.append("Success")
                HostName.append(Host)
                Server.append(GetDefaultServer())

                Result.append(HostName)
                Result.append(ServerStat)
                Result.append(Addr)
                Result.append(Server)

                #Main.append(Result)

                #return Main
		return Result

#---------------------------------------------------------------------------
# Resolve os nomes passados via o servidor DNS escolhido, no caso de algum
# tipo de erro o status da pesquisa sera: "Failed".

def ResolveViaServer(Hosts):

	ServerName = GetPassedServer()
	Main = []
	
	
	for host in Hosts:
		
		Lines = os.popen("host {0} {1} | grep '{2} has address' | wc -l".format( host, ServerName, host)).read()
		Lines = Lines.strip("\n")
		Lines = int(Lines)

		if Lines == 1:
			Result = ResolveOne(host, IfServerIsDefault())			
			Main.append(Result)

		elif Lines != 1 and Lines != 0:
			Result = ResolveSeveral(host, IfServerIsDefault())
			Main.append(Result)

		elif Lines == 0:
			#print("Chegou aqui")
		
			Result = []
			Addr = []
			ServerStat = []
			HostName = []
			Server = []			

			HostName.append(host)
                        ServerStat.append("Failed")	
			Addr.append("N/A")
			Server.append(ServerName)

			Result.append(HostName)
			Result.append(ServerStat)
			Result.append(Addr)
			Result.append(Server)

			Main.append(Result)
			

	return Main

#---------------------------------------------------------------------------
# Resolve os nomes passados via o servidor DNS escolhido, no caso de algum
# tipo de erro o status da pesquisa sera: "Failed"

def ResolveViaDefault(Hosts):

	Main = []
	ServerName = GetDefaultServer()	
	
	for host in Hosts:

		Lines = os.popen("host {0} | grep '{1} has address' | wc -l".format(host,host)).read()
		Lines = Lines.strip("\n")
		Lines = int(Lines)	

		if Lines == 1:
			Result = ResolveOne(host, IfServerIsDefault())			
			Main.append(Result)

		elif Lines != 1 and Lines != 0:
			Result = ResolveSeveral(host, IfServerIsDefault())
			Main.append(Result)

		elif Lines == 0:
			Result = []
                        Addr = []
                        ServerStat = []
                        HostName = []
                        Server = []

                        HostName.append(host)
                        ServerStat.append("Failed")
                        Addr.append("N/A")
                        Server.append(ServerName)

                        Result.append(HostName)
                        Result.append(ServerStat)
                        Result.append(Addr)
                        Result.append(Server)

                        Main.append(Result)	

	return Main

#---------------------------------------------------------------------------
# Resolve o nome dos usuarios utilizando servidor passado ou utilizando
# o servidor padrao.

def  HostResolve(Bool,Hosts):

	if Bool == 1:
		Result = ResolveViaServer(Hosts)

	elif Bool == 0:
		Result = ResolveViaDefault(Hosts)

	return Result

#---------------------------------------------------------------------------
# Constroi o JSON que sera enviado para indexacao no AvantData, tal JSON 
# e construido baseado nos resultados da query DNS.

def JSONConstruct(Result,time):

	LogInput = {}
	i=0
	while i <= int(sys.argv[2])-1:
	
	       	LogInput["Host"] = Result[i][0]
		LogInput["Status"] = Result[i][1]
		LogInput["Host IP"] = Result[i][2]
		LogInput["DNS Server"] = Result[i][3]
	
	        i += 1
	
	GenerateTime = os.popen("date +%s%3N").read()
	GenerateTime = GenerateTime.strip("\n")
	LogInput["GenerateTime"] = GenerateTime
	LogInput["Response Time"] = time

	Response = json.dumps(LogInput, ensure_ascii=False)
	return Response
	#print(Response)

#----------------------------------------------------------------------------

then = time.time()
Result = HostResolve(IfServerIsDefault(),GetHosts())
now = time.time()
#Response = JSONConstruct(HostResolve(IfServerIsDefault(),GetHosts()))
Response = JSONConstruct(Result,now-then)
print(Response)

#print(Result)
#print(len(Result))
#print(sys.argv[2])
#print(Result[0][0])
#print(Result[0][1])
#print(Result[0][2])
#print(Result[0][3])
#print(Result[1][0])
#print(Result[1][1])
#print(Result[1][2])
#print(Result[1][3])
#print(Result[1])
#print(Result[1])
