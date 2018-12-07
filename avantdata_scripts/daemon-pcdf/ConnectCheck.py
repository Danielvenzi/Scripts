import os
import sys

# IP - IP cuja conexão com será testada
# SIZE - Tamanho máximo do arquivo escrito no sistema em bytes

#IP = sys.argv[1] 
#SIZE = sys.argv[2]

# Pega as linhas do arquivo de configuração que tem os parsers que mandam logs pela rede
def getNetFiles(fileContent):
	resultArray = []
	
	NET_IN = os.popen("echo '{0}' | grep NetScriptsIN".format(fileContent)).read()
	NET_IN = NET_IN.strip("\n")
	NET_OUT = os.popen("echo '{0}' | grep NetScriptsOUT".format(fileContent)).read()
	NET_OUT = NET_OUT.strip("\n")
	NET_COUNT = NET_IN.count(":")
	NET_STOP = int(NET_COUNT)+1
	
	resultArray.append(NET_IN)
	resultArray.append(NET_OUT)
	resultArray.append(NET_STOP)

	#print(resultArray)
	return resultArray

# Pega as linhas do arquivo de configuração que tem os parsers que escrevem os logs no sistema
def getCachewFiles(fileContent):
	resultArray = []

	CACHE_IN = os.popen("echo '{0}' | grep CacheWriteIN".format(fileContent)).read()
	CACHE_IN = CACHE_IN.strip("\n")
	CACHE_OUT = os.popen("echo '{0}' | grep CacheWriteOUT".format(fileContent)).read()
	CACHE_OUT = CACHE_OUT.strip("\n")
	CACHE_COUNT = CACHE_IN.count(":")
	CACHE_STOP = int(CACHE_COUNT)+1

	resultArray.append(CACHE_IN)
	resultArray.append(CACHE_OUT)
	resultArray.append(CACHE_STOP)

	#print(resultArray)
	return resultArray	

# Pega as linhas do arquivo de configuração que tem os parsers que lêem os logs do sistema
def getCacherFiles(fileContent):
	resultArray = []

	CACHER_IN = os.popen("echo '{0}' | grep CacheReadIN".format(fileContent)).read()
	CACHER_IN = CACHER_IN.strip("\n")
	CACHER_OUT = os.popen("echo '{0}' | grep CacheReadOUT".format(fileContent)).read()
	CACHER_OUT = CACHER_OUT.strip("\n")
	CACHER_COUNT = CACHER_IN.count(":")
	CACHER_STOP = int(CACHER_COUNT)+1

	resultArray.append(CACHER_IN)
	resultArray.append(CACHER_OUT)
	resultArray.append(CACHER_STOP)

	#print(resultArray)
	return resultArray 
	
# Separa a linha em arquivos individuais
def lineProcess(fileArray,separatorCount):
	separatorCount = int(separatorCount)
	separatorCount += 1
	finalArray = []
	InArray = []
	OutArray = []
	K=0
	I=2
	J=2
	while I <= separatorCount:
		if I >= separatorCount:
			while J <= separatorCount-1:
				files = os.popen("echo '{0}' | cut -d: -f{1}".format(fileArray[K],J)).read()
				files = files.strip("\n")

				OutArray.append(files)
				J+=1
		elif I <= separatorCount:
			files = os.popen("echo '{0}' | cut -d: -f{1}".format(fileArray[K],I)).read()
			files = files.strip("\n")

			InArray.append(files)	
			if I == separatorCount-1:
			   K += 1
			
		I+=1
	
	finalArray.append(InArray)
	finalArray.append(OutArray)

	return finalArray

# Processa as linhas lidas do arquivo de configuração e separara os mesmos em arquivos diferentes
def readConfig():
	fileContent = os.popen("cat ./ConnectCheck_config").read()
	fileContent = fileContent.strip("\n")

	resultNetArray = getNetFiles(fileContent)
	resultCachewArray = getCachewFiles(fileContent)
	resultCacherArray = getCacherFiles(fileContent)

	counter = resultNetArray[2]
	resultArray = [resultNetArray, resultCachewArray, resultCacherArray]

	NetFiles = ""
	CachewFiles = ""
	CacherFiles = ""
	
	L = 0
	
	for configLine in resultArray:
		if L == 0:
			NetFiles = lineProcess(configLine,counter)
		elif L == 1:
			CachewFiles = lineProcess(configLine,counter)
		elif L == 2:
			CacherFiles = lineProcess(configLine,counter)
	
		L+=1

	resultFiles = [NetFiles, CachewFiles, CacherFiles]
	return resultFiles

# Verifica a conexão a internet
def connectCheck(ipAddr):
	stateOfConnect = os.popen("ping -c 1 {0} &> /dev/null ; echo $?".format(ipAddr)).read()
	stateOfConnect = stateOfConnect.strip("\n")
	
	if int(stateOfConnect) == 0:
		boolean = "true"

	elif int(stateOfConnect) != 0:
		boolean = "false"

	return boolean

# Checa o tamanho do arquivo do sistema onde serão salvos os logs
def checkSize(fileMaxSize,fileName):
	fileSize = os.popen("ls -l {0} | cut -d' ' -f5").read()
	fileSize = fileSize.strip("\n")

	if fileSize <= fileMaxSize:
		boolean = false
	elif fileSize > fileMaxSize:
		boolean = true

	return boolean

# Pega o array de elementos geral, e retorna os elementos de acordo com a necessidade
def moveSpecificFiles(resultFiles, Type):

	if Type == "NetIN":
		resultArray = resultFiles[0][0]

	elif Type == "NetOUT":
		resultArray = resultFiles[0][1]

	elif Type == "CachewIN":
		resultArray = resultFiles[1][0]

	elif Type == "CachewOUT":
		resultArray = resultFiles[1][1]

	elif Type == "CacherIN":
		resultArray = resultFiles[2][0]

	elif Type == "CacherOut":
		resultArray = resultFiles[2][0]
		
	return resultArray

# Função principal que junta todas e executa a "Máquina de estados"
def mainLoop():

	result = readConfig()
	booleanNet = ""
	booleanFile = ""
while True:

	os.system("mv /etc/logstash/conf.d /etc/logstash/desativados")
	state = "NET_IN"

	if state == "NET_IN":
		files = movespecificArray(result, NetIN)
		I=0
		while I <= len(files)-1:
			os.system("mv {0} /etc/logstash/conf.d".format(files[I]))
			I+=1
		
		booleanNet = connectCheck(sys.argv[1])		
		if booleanNet == "true":
			state = "NET_IN"
		elif booleanNet == "false":
			state = "NET_OUT"


	elif state == "NET_OUT":
		files = movespecificArray(result, NetOUT)
		I=0
                while I <= len(files)-1:
                        os.system("mv {0} /etc/logstash/desativados".format(files[I]))
                        I+=1

                booleanNet = connectCheck(sys.argv[1])
                if booleanNet == "true":
                        state = "NET_IN"
                elif booleanNet == "false":
                        state = "CACHEW_IN"

	elif state == "CACHEW_IN":
		files = movespecificArray(result, CachewIN)
		I=0
                while I <= len(files)-1:
                        os.system("mv {0} /etc/logstash/conf.d".format(files[I]))
                        I+=1

                booleanNet = connectCheck(sys.argv[1])
                if booleanNet == "true":
                        state = "CACHEW_OUT"
                elif booleanNet == "false":
                        state = "CACHEW_IN"
			I = 0
			while I <= len(files)-1:
				booleanFile = checkSize(sys.argv[2],files[I])
				

	elif state == "CACHEW_OUT":
		files = movespecificArray(result, CachewOUT)

	elif state == "CACHER_IN":
		files = movespecificArray(result, CacherIN)

	elif state == "CACHER_OUT":
		files = movespecificArray(result, CacherOUT)





# ---------------------- Seção de testes -------------------------- #

result = readConfig()
print(result)

