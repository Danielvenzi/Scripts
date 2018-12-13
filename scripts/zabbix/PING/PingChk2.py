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

<<<<<<< HEAD
#-------------------------------------------------------------
# Ping os hosts passados.

def PingHosts():




print(GetHosts())
=======
#------------------------------------------------------------
# Checa se os pings se o ping foi feito com sucesso.

def PingErr(Iterator,Hosts):

	ping = os.system("ping -c 1 {0} > res".format(Hosts[Iterator]))
	#os.system("cat ./res")
	Received = str(os.popen("cat ./res | grep transmitted |grep -Po 'transmitted, \K\d{1}'").read())
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
                PingTTL = str(os.popen("cat ./res | grep '64 bytes' | grep -Po 'time=\K\d{1,}.\d{1,}'").read())
                PingTTL = PingTTL.strip("\n")
                PingTime = str(os.popen("cat ./res | grep '64 bytes' | grep -Po 'time=\K\d{1,}.\d{1,}'").read())
                PingTime = PingTime.strip("\n")

                Dicionary["Host {0}".format(i+1)] = Hosts[i]
                Dicionary["Host {0} TTL".format(i+1)] = PingTTL
                Dicionary["Host {0} RTT".format(i+1)] = PingTime
                Dicionary["Host {0} Status".format(i+1)] = "Success"
                #print(Dicionary)

            elif Bool == 0:
                Dicionary["Host {0}".format(i+1)] = Hosts[i]
                Dicionary["Host {0} Status".format(i+1)] = "Failed"
                #print(Dicionary)

            i += 1

        GenerateTime = os.popen("date +%s%3N").read()
        GenerateTime = GenerateTime.strip("\n")

        Dicionary["Hosts"] = Hosts
        Dicionary["GenerateTime"] = GenerateTime

        Response = json.dumps(Dicionary, ensure_ascii=False)
        print(Response)



#print(GetHosts())
PingHosts(GetHosts())
>>>>>>> 4041db0d0d34c17359ce4666d3e70abcef26b7db
