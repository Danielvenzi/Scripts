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

#------------------------------------------------------------
# Checa se os pings se o ping foi feito com sucesso.

def PingErr(Iterator,Hosts):

	ping = os.system("ping -c 1 {0} > /usr/local/bin/res".format(Hosts[Iterator]))
	#os.system("cat ./res")
	Received = str(os.popen("cat /usr/local/bin/res | grep transmitted |grep -Po 'transmitted, \K\d{1}'").read())
	Received = Received.strip("\n")
	return Received

#------------------------------------------------------------
# Ping os hosts passados.

def PingHosts(Hosts):
    
        Dicionary={}
        i=0

        while i <= len(Hosts)-1:

            #print(Dict)
            Bool = int(PingErr(i,Hosts))
            #print(Bool)
            if Bool == 1:
                PingTTL = str(os.popen("cat /usr/local/bin/res | grep '64 bytes' | grep -Po 'time=\K\d{1,}.\d{1,}'").read())
                PingTTL = PingTTL.strip("\n")
                PingTime = str(os.popen("cat /usr/local/bin/res | grep '64 bytes' | grep -Po 'time=\K\d{1,}.\d{1,}'").read())
                PingTime = PingTime.strip("\n")

                Dicionary["Host"] = Hosts[i]
                #Dicionary["TTL"] = PingTTL
                Dicionary["Response Time"] = PingTime
                Dicionary["Status"] = "Success"
                #print(Dicionary)

            elif Bool == 0:
                Dicionary["Host"] = Hosts[i]
                Dicionary["Status"] = "Failed"
                #print(Dicionary)

            i += 1

        GenerateTime = os.popen("date +%s%3N").read()
        GenerateTime = GenerateTime.strip("\n")

        #Dicionary["Hosts"] = Hosts
        Dicionary["GenerateTime"] = GenerateTime

	os.system("rm -f /usr/local/bin/res")
        Response = json.dumps(Dicionary, ensure_ascii=False)
        print(Response)



#print(GetHosts())
PingHosts(GetHosts())
